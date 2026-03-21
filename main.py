"""
Bot de Hidratación - Main
Envía recordatorios de hidratación via Telegram
"""
import asyncio
import logging
from datetime import datetime

from telegram import Bot
from telegram.error import TelegramError

from config import (
    TOKEN, CHAT_ID, HORARIOS, MENSAJE, MENSAJE_INICIO, 
    INTERVALO_CHECK, LOG_LEVEL
)

# Configurar logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HidratacionBot:
    """Bot de recordatorios de hidratación"""
    
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.bot = None
        self.ya_enviado = set()
        self._ultimo_reset = None
    
    async def iniciar(self):
        """Inicializa el bot y envía mensaje de bienvenida"""
        try:
            self.bot = Bot(token=self.token)
            # Verificar conexión
            await self.bot.get_me()
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=MENSAJE_INICIO
            )
            logger.info(f"Bot iniciado correctamente. Enviando recordatorios a chat {self.chat_id}")
        except TelegramError as e:
            logger.error(f"Error al iniciar el bot: {e}")
            raise
    
    async def enviar_recordatorio(self):
        """Envía mensaje de hidratación si es la hora correcta"""
        ahora = datetime.now()
        hora_actual = ahora.strftime("%H:%M")
        fecha_actual = ahora.date()
        
        # Reset diario a medianoche
        if self._ultimo_reset != fecha_actual:
            self.ya_enviado.clear()
            self._ultimo_reset = fecha_actual
            logger.info("Reseteando recordatorios para nuevo día")
        
        if hora_actual in HORARIOS and hora_actual not in self.ya_enviado:
            try:
                await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=MENSAJE
                )
                self.ya_enviado.add(hora_actual)
                logger.info(f"✅ Recordatorio enviado a las {hora_actual}")
            except TelegramError as e:
                logger.error(f"Error al enviar mensaje: {e}")
    
    async def ejecutar(self):
        """Bucle principal del bot"""
        await self.iniciar()
        
        while True:
            try:
                await self.enviar_recordatorio()
                await asyncio.sleep(INTERVALO_CHECK)
            except TelegramError as e:
                logger.error(f"Error de Telegram: {e}")
                await asyncio.sleep(INTERVALO_CHECK * 3)  # Espera más larga en caso de error
            except Exception as e:
                logger.error(f"Error inesperado: {e}")
                await asyncio.sleep(INTERVALO_CHECK)


async def main():
    """Punto de entrada"""
    logger.info("🚀 Iniciando bot de hidratación...")
    bot = HidratacionBot(TOKEN, CHAT_ID)
    await bot.ejecutar()


if __name__ == "__main__":
    asyncio.run(main())
