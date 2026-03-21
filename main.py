"""
Bot de Hidratación - Main
Envía recordatorios de hidratación via Telegram
"""
import asyncio
import logging
from datetime import datetime

from telegram import Bot

from config import TOKEN, CHAT_ID, HORARIOS, MENSAJE, MENSAJE_INICIO, INTERVALO_CHECK

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
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
    
    async def iniciar(self):
        """Inicializa el bot y envía mensaje de bienvenida"""
        self.bot = Bot(token=self.token)
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=MENSAJE_INICIO
        )
        logger.info(f"Bot iniciado. Enviando recordatorios a chat {self.chat_id}")
    
    async def enviar_recordatorio(self):
        """Envía mensaje de hidratación si es la hora correcta"""
        ahora = datetime.now().strftime("%H:%M")
        
        if ahora in HORARIOS and ahora not in self.ya_enviado:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=MENSAJE
            )
            self.ya_enviado.add(ahora)
            logger.info(f"Recordatorio enviado a las {ahora}")
            await asyncio.sleep(60)  # Evitar doble envío
        
        elif ahora not in HORARIOS:
            # Reset a medianoche o cuando sale del rango
            if ahora < HORARIOS[0]:
                self.ya_enviado.clear()
    
    async def ejecutar(self):
        """Bucle principal del bot"""
        await self.iniciar()
        
        while True:
            try:
                await self.enviar_recordatorio()
                await asyncio.sleep(INTERVALO_CHECK)
            except Exception as e:
                logger.error(f"Error en el bucle: {e}")
                await asyncio.sleep(INTERVALO_CHECK)


async def main():
    """Punto de entrada"""
    logger.info("Iniciando bot de hidratación...")
    bot = HidratacionBot(TOKEN, CHAT_ID)
    await bot.ejecutar()


if __name__ == "__main__":
    asyncio.run(main())
