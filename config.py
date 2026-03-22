"""
Bot de Hidratación - Archivo de Configuración
Centraliza todas las variables configurables
"""
import os

# Configuración del Bot
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7951251109:AAF2uaFPO4N0MsWhmesFhpnIgyjwXMrcZDM")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "6067040288")

# Horarios de hidratación (formato 24h)
# Edita esta lista para personalizar los horarios
HORARIOS = [
    "05:30", "07:00", "08:30", "10:00", "11:30",
    "13:00", "14:30", "16:00", "17:30", "19:00",
    "20:30", "22:00", "23:30", "00:15"
]

# Mensaje de hidratación
# Usa emojis y texto motivador
MENSAJE = "💧 ¡Hora de tomar agua! Bebe 250 ml y mantente saludable. 🚰💪"

# Configuración técnica
INTERVALO_CHECK = 20  # Segundos entre verificaciones
MENSAJE_INICIO = "🟢 Bot de hidratación iniciado. Recibirás alertas durante el día."
