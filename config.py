"""
Configuración del Bot de Hidratación
Carga variables de entorno con valores por defecto
"""
import os
from pathlib import Path

# Cargar desde .env si existe
from dotenv import load_dotenv

# Buscar .env en el directorio actual o padre
env_path = Path(__file__).resolve().parent / '.env'
if not env_path.exists():
    env_path = Path(__file__).resolve().parent.parent / '.env'

load_dotenv(env_path)

# ============================================
# CONFIGURACIÓN DEL BOT
# ============================================

# Token del bot de Telegram (obtener de @BotFather)
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# Chat ID(s) destino - puede ser uno o múltiples separados por coma
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
CHAT_IDS = os.getenv('TELEGRAM_CHAT_IDS', CHAT_ID)

# ============================================
# HORARIOS DE RECORDATORIOS (formato 24h)
# ============================================

# Horarios por defecto - cada 1.5 horas desde las 6am hasta las 11pm
HORARIOS = [
    "06:00", "07:30", "09:00", "10:30",
    "12:00", "13:30", "15:00", "16:30",
    "18:00", "19:30", "21:00", "22:30"
]

# ============================================
# MENSAJES
# ============================================

# Mensaje de recordatorio principal
MENSAJE = os.getenv(
    'MENSAJE_HIDRATACION',
    "💧 *¡Hora de hidratarse!*\n\n"
    "Bebe un vaso de agua (250ml) para mantenerte saludable.\n\n"
    "💪 *Beneficios del agua:*\n"
    "• Mantiene tu energía\n"
    "• Mejora tu concentración\n"
    "• Detoxifica tu cuerpo\n\n"
    "_Stay hydrated, stay healthy!_ 🚰"
)

# Mensaje de inicio
MENSAJE_INICIO = (
    "✅ *Bot de Hidratación Activado*\n\n"
    "Te enviaré recordatorios para mantenerte hidratado a lo largo del día.\n\n"
    f"📅 *Horarios activos:* {', '.join(HORARIOS)}\n"
    "💧 ¡Prepárate para recordar beber agua!"
)

# Mensaje de error
MENSAJE_ERROR = "⚠️ Error al enviar el recordatorio. Reintentando..."

# ============================================
# CONFIGURACIÓN DE INTERVALOS
# ============================================

# Intervalo de verificación en segundos (default: 60 segundos)
INTERVALO_CHECK = int(os.getenv('INTERVALO_CHECK', '60'))

# Segundos de espera después de enviar un recordatorio para evitar duplicados
ESPERA_POST_ENVIO = int(os.getenv('ESPERA_POST_ENVIO', '5'))

# ============================================
# CONFIGURACIÓN DE LOGGING
# ============================================

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

# ============================================
# VALIDACIÓN
# ============================================

def validar_config():
    """Valida que la configuración sea correcta"""
    errores = []
    
    if not TOKEN:
        errores.append("TELEGRAM_BOT_TOKEN no configurado")
    
    if not CHAT_ID and not CHAT_IDS:
        errores.append("TELEGRAM_CHAT_ID no configurado")
    
    if errores:
        raise ValueError(f"Errores de configuración:\n" + "\n".join(errores))
    
    return True


# Validar al importar
if __name__ != "__main__":
    try:
        validar_config()
    except ValueError as e:
        print(f"⚠️ Advertencia de configuración: {e}")
