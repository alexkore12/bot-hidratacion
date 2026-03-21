"""
Bot de Hidratación - Archivo de Configuración
Centraliza todas las variables configurables
"""
import os
from pathlib import Path

# Cargar variables de entorno desde archivo .env si existe
from dotenv import load_dotenv

# Buscar .env en el directorio del proyecto
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Configuración del Bot - Se requieren variables de entorno
# NO hardcodear tokens en producción
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Validar configuración requerida
if not TOKEN or not CHAT_ID:
    raise ValueError(
        "ERROR: TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID son requeridos. "
        "Crea un archivo .env o establece las variables de entorno."
    )

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

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
