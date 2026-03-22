"""
Bot de Hidratación - Main
Envía recordatorios de hidratación via Telegram
Versión mejorada 2.0 - Con soporte para múltiples chats, mejor logging y manejo de errores
"""
import asyncio
import logging
import os
import signal
import sys
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError

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
                    logger.info(f"✅ Recordatorio enviado a {chat_id} a las {ahora}")
                    
                    # Evitar doble envío
                    await asyncio.sleep(2)
                    
                except TelegramError as e:
                    logger.error(f"❌ Error al enviar a {chat_id}: {e}")
                except Exception as e:
                    logger.error(f"❌ Error inesperado enviando a {chat_id}: {e}")
    
    async def verificar_conexion(self):
        """Verifica que el bot esté conectado"""
        try:
            await self.bot.get_me()
            return True
        except TelegramError:
            logger.error("⚠️ Conexión perdida. Reconectando...")
            self.bot = Bot(token=self.token)
            return False
    
    async def ejecutar(self):
        """Bucle principal del bot con manejo de errores"""
        await self.iniciar()
        
        logger.info(f"🚀 Bot ejecutándose. Horarios: {HORARIOS}")
        logger.info(f"📋 Intervalo de verificación: {INTERVALO_CHECK} segundos")
        
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
                await asyncio.sleep(INTERVALO_CHECK * 2)  # Espera más larga en caso de error
        
        logger.info("👋 Bot detenido")
    
    def detener(self):
        """Detiene el bot gracefulmente"""
        logger.info("🛑 Solicitando parada del bot...")
        self.ejecutando = False


async def main():
    """Punto de entrada con manejo de señales"""
    logger.info("=" * 50)
    logger.info("🤖 Iniciando Bot de Hidratación v2.0")
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
    
    # Manejo de señales para shutdown graceful
    def signal_handler(sig, frame):
        logger.info("📡 Señal de parada recibida")
        bot.detener()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        await bot.ejecutar()
    except KeyboardInterrupt:
        logger.info("🛑 Interrupción de teclado")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
