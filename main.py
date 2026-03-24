"""
Bot de Hidratación - Main v3.0
Con soporte multi-chat, persistencia SQLite, comandos interactivos y recordatorios
"""
import asyncio
import logging
import os
import signal
import sys
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import TOKEN, HORARIOS, MENSAJE, MENSAJE_INICIO, INTERVALO_CHECK
from database import get_db
from bot_commands import COMMAND_HANDLERS

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot-hidratacion.log') if os.path.exists('/tmp') else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)


class HidratacionBot:
    """Bot de recordatorios de hidratación con persistencia y comandos interactivos"""

    def __init__(self, token: str, chat_ids: list):
        self.token = token
        self.chat_ids = [str(cid).strip() for cid in chat_ids if cid]
        self.bot_instance = None
        self.app = None
        self.ejecutando = True
        self._ya_enviado = {}  # Tracking de recordatorios por chat

        # Inicializar base de datos
        self.db = get_db()
        logger.info(f"✓ Base de datos inicializada")

        # Inicializar tracking de envíos
        for chat_id in self.chat_ids:
            self._ya_enviado[chat_id] = set()

    async def iniciar(self):
        """Inicializa el bot y envía mensaje de bienvenida"""
        self.bot_instance = Bot(token=self.token)

        try:
            me = await self.bot_instance.get_me()
            logger.info(f"Bot conectado: @{me.username} (ID: {me.id})")
        except TelegramError as e:
            logger.error(f"Error al conectar con Telegram: {e}")
            raise

        # Enviar mensaje de inicio a todos los chats
        for chat_id in self.chat_ids:
            try:
                await self.bot_instance.send_message(
                    chat_id=chat_id,
                    text=MENSAJE_INICIO
                )
                logger.info(f"✅ Bot iniciado para chat {chat_id}")
            except TelegramError as e:
                logger.error(f"❌ Error enviando a chat {chat_id}: {e}")

    async def enviar_recordatorio(self):
        """Envía recordatorios programados a todos los chats"""
        ahora = datetime.now().strftime("%H:%M")

        # Verificar si es hora de enviar
        if ahora not in HORARIOS:
            if ahora < HORARIOS[0]:
                # Reset a medianoche
                for chat_id in self.chat_ids:
                    self._ya_enviado[chat_id] = set()
            return

        for chat_id in self.chat_ids:
            if ahora not in self._ya_enviado.get(chat_id, set()):
                try:
                    # Obtener progreso actual
                    goal_info = self.db.check_daily_goal(chat_id)
                    total = goal_info['total_ml']
                    goal = goal_info['goal_ml']
                    remaining = goal - total

                    mensaje = (
                        f"💧 *¡Hora de hidratarse!*\n\n"
                        f"Bebe un vaso de agua (250ml) para mantenerte saludable.\n\n"
                        f"📊 *Tu progreso:*\n"
                        f"• Hoy: {total}ml / {goal}ml\n"
                    )

                    if remaining > 0:
                        mensaje += f"• Faltan: {remaining}ml\n"
                    else:
                        mensaje += f"✅ *¡Meta alcanzada!* ¡Sigue así!\n"

                    mensaje += (
                        f"\n💪 *Beneficios del agua:*\n"
                        f"• Mantiene tu energía\n"
                        f"• Mejora tu concentración\n"
                        f"• Detoxifica tu cuerpo\n\n"
                        f"_Stay hydrated, stay healthy!_ 🚰"
                    )

                    await self.bot_instance.send_message(
                        chat_id=chat_id,
                        text=mensaje,
                        parse_mode='Markdown'
                    )
                    self._ya_enviado[chat_id].add(ahora)
                    logger.info(f"✅ Recordatorio enviado a {chat_id} a las {ahora}")

                    await asyncio.sleep(2)

                except TelegramError as e:
                    logger.error(f"❌ Error enviando a {chat_id}: {e}")
                except Exception as e:
                    logger.error(f"❌ Error inesperado: {e}")

    async def verificar_conexion(self):
        """Verifica que el bot esté conectado"""
        try:
            await self.bot_instance.get_me()
            return True
        except TelegramError:
            logger.warning("⚠️ Conexión perdida. Reconectando...")
            self.bot_instance = Bot(token=self.token)
            return False

    async def recordatorio_loop(self):
        """Bucle de recordatorios automáticos (corre en paralelo al app)"""
        await self.iniciar()

        logger.info(f"🚀 Recordatorios activos. Horarios: {HORARIOS}")
        logger.info(f"📋 Intervalo de verificación: {INTERVALO_CHECK}s")

        while self.ejecutando:
            try:
                await self.verificar_conexion()
                await self.enviar_recordatorio()
                await asyncio.sleep(INTERVALO_CHECK)

            except asyncio.CancelledError:
                logger.info("🛑 Bucle de recordatorios detenido")
                break
            except Exception as e:
                logger.error(f"❌ Error en bucle de recordatorios: {e}")
                await asyncio.sleep(INTERVALO_CHECK * 2)

        logger.info("👋 Bucle de recordatorios terminado")

    def detener(self):
        """Detiene el bot gracefulmente"""
        logger.info("🛑 Solicitando parada del bot...")
        self.ejecutando = False

    def run(self):
        """Ejecuta el bot con comandos y recordatorios"""
        # Build application with command handlers
        app = (
            Application.builder()
            .token(self.token)
            .read_timeout(30)
            .write_timeout(30)
            .build()
        )

        # Registrar comandos
        for cmd_name, handler in COMMAND_HANDLERS.items():
            app.add_handler(CommandHandler(cmd_name, handler))

        # Handler por defecto para mensajes no reconocidos
        app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                self._handle_unknown
            )
        )

        # Iniciar recordatorios en segundo plano
        async def start_all():
            reminder_task = asyncio.create_task(self.recordatorio_loop())
            await app.initialize()
            await app.start()
            await app.run_polling(drop_pending_updates=True)

            # Cleanup
            self.detener()
            reminder_task.cancel()

        asyncio.run(start_all())

    @staticmethod
    async def _handle_unknown(update, context):
        """Maneja mensajes que no son comandos"""
        await update.message.reply_text(
            "🤔 No entendí ese mensaje.\n"
            "Usa `/help` para ver los comandos disponibles.",
            parse_mode='Markdown'
        )


async def main():
    """Punto de entrada principal"""
    logger.info("=" * 50)
    logger.info("🤖 Bot de Hidratación v3.0")
    logger.info("=" * 50)

    # Obtener configuración
    chat_ids_raw = os.getenv('TELEGRAM_CHAT_IDS', os.getenv('TELEGRAM_CHAT_ID', ''))
    if not chat_ids_raw:
        logger.error("❌ No se especificó TELEGRAM_CHAT_ID o TELEGRAM_CHAT_IDS")
        sys.exit(1)

    chat_ids = [cid.strip() for cid in chat_ids_raw.split(',') if cid.strip()]
    if not chat_ids:
        logger.error("❌ Lista de chat IDs vacía")
        sys.exit(1)

    token = os.getenv('TELEGRAM_BOT_TOKEN', TOKEN)
    if not token:
        logger.error("❌ No se especificó TELEGRAM_BOT_TOKEN")
        sys.exit(1)

    logger.info(f"📋 Chat IDs configurados: {chat_ids}")

    # Crear y ejecutar bot
    bot = HidratacionBot(token, chat_ids)

    # Manejo de señales
    def signal_handler(sig, frame):
        logger.info("📡 Señal de parada recibida")
        bot.detener()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("🛑 Interrupción de teclado")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
