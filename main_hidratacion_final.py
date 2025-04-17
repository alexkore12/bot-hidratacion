import asyncio
from telegram import Bot
from datetime import datetime

# Token y Chat ID actualizados
TOKEN = "7951251109:AAF2uaFPO4N0MsWhmesFhpnIgyjwXMrcZDM"
CHAT_ID = "6067040288"

# Nuevos horarios de hidratación (formato 24h)
HORARIOS = [
    "05:30", "07:00", "08:30", "10:00", "11:30",
    "13:00", "14:30", "16:00", "17:30", "19:00",
    "20:30", "22:00", "23:30", "00:15"
]

# Mensaje de hidratación
MENSAJE = "💧 ¡Hora de tomar agua, Brayan! Bebe 250 ml y mantente saludable. 🚰💪"

async def enviar_mensaje(bot):
    ya_enviado = set()
    while True:
        ahora = datetime.now().strftime("%H:%M")
        if ahora in HORARIOS and ahora not in ya_enviado:
            await bot.send_message(chat_id=CHAT_ID, text=MENSAJE)
            ya_enviado.add(ahora)
            await asyncio.sleep(60)
        elif ahora not in HORARIOS:
            ya_enviado.clear()
        await asyncio.sleep(20)

async def main():
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="🟢 Bot de hidratación iniciado. Recibirás alertas durante el día.")
    await enviar_mensaje(bot)

if __name__ == "__main__":
    asyncio.run(main())
