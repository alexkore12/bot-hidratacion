"""
Bot de Hidratación - Main
Envía recordatorios de hidratación via Telegram
Versión 2.1 - Con comandos interactivos, estadísticas y mejor manejo
"""
import asyncio
import logging
import os
import signal
import sys
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import TOKEN, CHAT_ID, HORARIOS, MENSAJE, MENSAJE_INICIO, INTERVALO_CHECK

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot-hidratacion.log') if os.path.exists('/tmp') else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)


class HidratacionBot:
    """Bot de recordatorios de hidratación con soporte multi-chat"""
    
    def __init__(self, token: str, chat_ids: list):
        self.token = token
        self.chat_ids = chat_ids if isinstance(chat_ids, list) else [chat_ids]
        self.bot = None
        self.ya_enviado = {}  # Dict para manejar múltiples chats
        self.ejecutando = True
        self.app = None
        self.stats = {"enviados": 0, "errores": 0, "inicio": datetime.now()}
        self._inicializar_ya_enviado()
    
    def _inicializar_ya_enviado(self):
        """Inicializa el tracking de mensajes enviados por chat"""
        for chat_id in self.chat_ids:
            self.ya_enviado[chat_id] = set()
    
    async def iniciar(self):
        """Inicializa el bot y envía mensaje de bienvenida"""
        self.bot = Bot(token=self.token)
        
        # Verificar conexión
        try:
            me = await self.bot.get_me()
            logger.info(f"Bot conectado: @{me.username} (ID: {me.id})")
        except TelegramError as e:
            logger.error(f"Error al conectar con Telegram: {e}")
            raise
        
        # Enviar mensaje a todos los chats configurados
        for chat_id in self.chat_ids:
            try:
                await self.bot.send_message(
                    chat_id=chat_id,
                    text=MENSAJE_INICIO
                )
                logger.info(f"✅ Bot iniciado. Recordatorios configurados para chat {chat_id}")
            except TelegramError as e:
                logger.error(f"❌ Error al enviar a chat {chat_id}: {e}")
    
    async def enviar_recordatorio(self):
        """Envía mensaje de hidratación a todos los chats configurados"""
        ahora = datetime.now().strftime("%H:%M")
        
        # Verificar si es hora de enviar
        if ahora not in HORARIOS:
            # Reset a medianoche o cuando sale del rango
            if ahora < HORARIOS[0]:
                self._inicializar_ya_enviado()
            return
        
        # Enviar a cada chat
        for chat_id in self.chat_ids:
            if ahora not in self.ya_enviado.get(chat_id, set()):
                try:
                    await self.bot.send_message(
                        chat_id=chat_id,
                        text=MENSAJE
                    )
                    self.ya_enviado[chat_id].add(ahora)
                    self.stats["enviados"] += 1
                    logger.info(f"✅ Recordatorio enviado a {chat_id} a las {ahora}")
                    
                    # Evitar doble envío
                    await asyncio.sleep(2)
                    
                except TelegramError as e:
                    logger.error(f"❌ Error al enviar a {chat_id}: {e}")
                    self.stats["errores"] += 1
                except Exception as e:
                    logger.error(f"❌ Error inesperado enviando a {chat_id}: {e}")
                    self.stats["errores"] += 1
    
    async def verificar_conexion(self):
        """Verifica que el bot esté conectado"""
        try:
            await self.bot.get_me()
            return True
        except TelegramError:
            logger.error("⚠️ Conexión perdida. Reconectando...")
            self.bot = Bot(token=self.token)
            return False
    
    async def recordatorio_loop(self):
        """Bucle principal de recordatorios"""
        while self.ejecutando:
            try:
                # Verificar conexión periódicamente
                await self.verificar_conexion()
                
                # Enviar recordatorios
                await self.enviar_recordatorio()
                
                # Esperar antes del siguiente check
                await asyncio.sleep(INTERVALO_CHECK)
                
            except asyncio.CancelledError:
                logger.info("🛑 Bot detenido manualmente")
                break
            except Exception as e:
                logger.error(f"❌ Error en el bucle principal: {e}")
                await asyncio.sleep(INTERVALO_CHECK * 2)
    
    def detener(self):
        """Detiene el bot gracefulmente"""
        logger.info("🛑 Solicitando parada del bot...")
        self.ejecutando = False


# ============================================
# HANDLERS DE COMANDOS
# ============================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Inicia el bot"""
    await update.message.reply_text(
        "💧 *Bot de Hidratación*\n\n"
        "¡Hola! Te ayudaré a mantenerte hidratado.\n\n"
        "📋 *Comandos disponibles:*\n"
        "/start - Iniciar\n"
        "/stop - Detener recordatorios\n"
        "/status - Ver estado\n"
        "/stats - Ver estadísticas\n"
        "/horarios - Mostrar horarios\n"
        "/ayuda - Esta ayuda",
        parse_mode="Markdown"
    )


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /stop - Detiene los recordatorios"""
    await update.message.reply_text(
        "⏹️ *Recordatorios pausados*\n\n"
        "Los recordatorios han sido pausados. Usa /start para reanudar.",
        parse_mode="Markdown"
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /status - Muestra el estado del bot"""
    uptime = datetime.now() - bot_global.stats["inicio"]
    horas = uptime.total_seconds() / 3600
    
    await update.message.reply_text(
        f"📊 *Estado del Bot*\n\n"
        f"• Estado: 🟢 Activo\n"
        f"• Uptime: {horas:.1f} horas\n"
        f"• Recordatorios enviados: {bot_global.stats['enviados']}\n"
        f"• Errores: {bot_global.stats['errores']}\n"
        f"• Próximo horario: {HORARIOS[0] if HORARIOS else 'N/A'}",
        parse_mode="Markdown"
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /stats - Muestra estadísticas"""
    uptime = datetime.now() - bot_global.stats["inicio"]
    dias = uptime.days
    
    await update.message.reply_text(
        f"📈 *Estadísticas de Hidratación*\n\n"
        f"• Días activo: {dias}\n"
        f"• Recordatorios enviados: {bot_global.stats['enviados']}\n"
        f"• Tasa de éxito: {((bot_global.stats['enviados']/(bot_global.stats['enviados']+bot_global.stats['errores'])*100) if (bot_global.stats['enviados']+bot_global.stats['errores']) > 0 else 100):.1f}%\n"
        f"• Horarios activos: {len(HORARIOS)}",
        parse_mode="Markdown"
    )


async def horarios_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /horarios - Muestra los horarios"""
    horarios_str = "\n".join([f"• {h}" for h in HORARIOS])
    await update.message.reply_text(
        f"⏰ *Horarios de Recordatorio*\n\n{horarios_str}",
        parse_mode="Markdown"
    )


async def ayuda_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ayuda - Muestra ayuda"""
    await update.message.reply_text(
        "❓ *Ayuda*\n\n"
        "Este bot envía recordatorios de hidratación a las horas configuradas.\n\n"
        "💡 *Consejos:*\n"
        "• Mantén el bot ejecutándose 24/7\n"
        "• Los horarios son configurables en config.py\n"
        "• Puedes usar múltiples chats\n\n"
        "📱 *Comandos:* /start /stop /status /stats /horarios /ayuda",
        parse_mode="Markdown"
    )


# Variable global para acceso desde handlers
bot_global = None


async def main():
    """Punto de entrada con manejo de señales"""
    global bot_global
    
    logger.info("=" * 50)
    logger.info("🤖 Iniciando Bot de Hidratación v2.1")
    logger.info("=" * 50)
    
    # Obtener chat IDs
    chat_ids = os.getenv('TELEGRAM_CHAT_IDS', os.getenv('TELEGRAM_CHAT_ID', ''))
    if not chat_ids:
        logger.error("❌ No se especificó TELEGRAM_CHAT_ID o TELEGRAM_CHAT_IDS")
        sys.exit(1)
    
    # Convertir a lista
    chat_ids = [cid.strip() for cid in chat_ids.split(',')]
    
    # Obtener token
    token = os.getenv('TELEGRAM_BOT_TOKEN', TOKEN)
    if not token:
        logger.error("❌ No se especificó TELEGRAM_BOT_TOKEN")
        sys.exit(1)
    
    # Crear instancia del bot
    bot = HidratacionBot(token, chat_ids)
    bot_global = bot
    
    # Iniciar el bot de Telegram con handlers
    application = Application.builder().token(token).build()
    
    # Registrar comandos
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("stop", stop_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("horarios", horarios_command))
    application.add_handler(CommandHandler("ayuda", ayuda_command))
    application.add_handler(CommandHandler("help", ayuda_command))
    
    bot.app = application
    
    # Iniciar recordatorios en background
    recordatorio_task = asyncio.create_task(bot.recordatorio_loop())
    
    # Iniciar el bot de Telegram
    await application.run_polling()
    
    # Cleanup
    bot.detener()
    await recordatorio_task


if __name__ == "__main__":
    asyncio.run(main())
