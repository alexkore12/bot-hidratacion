# 🤖 Bot de Hidratación

Bot de Telegram que envía recordatorios de hidratación a lo largo del día. **Versión 2.1** con comandos interactivos, estadísticas y mejor manejo de errores.

## 📋 Descripción

Este bot envía mensajes automatizados a intervalos específicos durante el día para recordar hidratarse. Fue diseñado para ayudar a mantener una rutina de hidratación saludable.

## 🛠️ Características

- ✅ Recordatorios automáticos configurables (default: cada 1.5 horas)
- ✅ Soporte para múltiples chats (separados por coma)
- ✅ **Comandos interactivos** (/start, /stop, /status, /stats, /horarios, /ayuda)
- ✅ **Estadísticas de envíos** en tiempo real
- ✅ Mensajes personalizados con Markdown
- ✅ Modo 24/7 con auto-reconexión
- ✅ Logging completo a archivo y consola
- ✅ Manejo graceful de señales (SIGINT/SIGTERM)
- ✅ Notificación de inicio con horarios activos

## 🚀 Instalación

### Prerrequisitos

- Python 3.9+
- Token de Bot de Telegram

### Pasos

1. **Clonar el repositorio:**
```bash
git clone https://github.com/alexkore12/bot-hidratacion.git
cd bot-hidratacion
```

2. **Crear entorno virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**

Crea un archivo `.env`:
```bash
# Obligatorio
TELEGRAM_BOT_TOKEN="tu_token_aqui"
TELEGRAM_CHAT_ID="tu_chat_id_aqui"

# Opcional - múltiples chats
# TELEGRAM_CHAT_IDS="chat1,chat2,chat3"

# Opcional
TELEGRAM_CHAT_IDS="123456789,987654321"
MENSAJE_HIDRATACION="💧 ¡Hora de beber agua!"
INTERVALO_CHECK=60
LOG_LEVEL=INFO
```

## ⚙️ Comandos Interactivos

El bot responde a los siguientes comandos de Telegram:

| Comando | Descripción |
|---------|-------------|
| `/start` | Iniciar el bot y mostrar ayuda |
| `/stop` | Pausar recordatorios |
| `/status` | Ver estado actual del bot |
| `/stats` | Ver estadísticas de envíos |
| `/horarios` | Mostrar horarios de recordatorio |
| `/ayuda` | Mostrar ayuda |
| `/help` | Mostrar ayuda (alias) |

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram | (requerido) |
| `TELEGRAM_CHAT_ID` | ID del chat destino (solo uno) | (requerido) |
| `TELEGRAM_CHAT_IDS` | IDs separados por coma (múltiples) | (opcional) |
| `MENSAJE_HIDRATACION` | Mensaje de recordatorio | Mensaje default |
| `INTERVALO_CHECK` | Segundos entre verificaciones | 60 |
| `LOG_LEVEL` | Nivel de logging | INFO |

### Personalizar Horarios

Edita la lista `HORARIOS` en `config.py`:

```python
HORARIOS = [
    "06:00", "07:30", "09:00", "10:30",
    "12:00", "13:30", "15:00", "16:30",
    "18:00", "19:30", "21:00", "22:30"
]
```

### Personalizar Mensaje

Usa la variable `MENSAJE_HIDRATACION` en `.env` o edita `config.py`:

```python
MENSAJE = "💧 ¡Hora de tomar agua! Bebe 250 ml y mantente saludable. 🚰💪"
```

El mensaje soporta Markdown:
- `*bold*`
- `_italic_`
- `•` bullet points

## 🐳 Docker

### Build

```bash
docker build -t bot-hidratacion .
```

### Ejecutar

```bash
docker run -d \
  --name bot-hidratacion \
  -e TELEGRAM_BOT_TOKEN="tu_token" \
  -e TELEGRAM_CHAT_ID="tu_chat_id" \
  bot-hidratacion
```

### Docker Compose

```yaml
version: '3.8'
services:
  bot:
    build: .
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - TELEGRAM_CHAT_IDS=${TELEGRAM_CHAT_IDS}
    volumes:
      - ./bot-hidratacion.log:/app/bot-hidratacion.log
```

## ☁️ Deploy en Render/Railway/Heroku

### Render/Railway

1. Conecta tu repositorio
2. Configura las variables de entorno:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_IDS`
3. Comando de inicio: `python main.py`

### Heroku

```bash
# Crear app
heroku create bot-hidratacion

# Configurar variables
heroku config:set TELEGRAM_BOT_TOKEN=tu_token
heroku config:set TELEGRAM_CHAT_IDS=tu_chat_id

# Desplegar
git push heroku main
```

## 📁 Estructura del Proyecto

```
bot-hidratacion/
├── main.py              # Código principal del bot (v2.1)
├── config.py           # Configuración centralizada
├── requirements.txt    # Dependencias Python
├── Procfile            # Para deploy en Railway/Render
├── .env.example        # Ejemplo de configuración
├── .gitignore
└── README.md           # Este archivo
```

## 🔧 Mantenimiento

### Verificar logs

```bash
# Local
python main.py

# Docker
docker logs -f bot-hidratacion

# Ver archivo de log
tail -f bot-hidratacion.log
```

### Reiniciar el bot

```bash
# Si el bot deja de funcionar
pkill -f main.py
python main.py

# Docker
docker restart bot-hidratacion
```

## ⚠️ Notas Importantes

- El bot funciona continuamente y debe estar siempre activo
- Asegúrate de que el token del bot tenga permisos para enviar mensajes
- El Chat ID debe ser un número (no @username)
- Usa `TELEGRAM_CHAT_IDS` para múltiples chats (separados por coma)
- El log se guarda en `bot-hidratacion.log` (en Docker, configura volumen)
- Los comandos /stop y /start son locales al chat, no detienen el servicio

## 🧪 Testing

### Verificar token

```bash
# Usando curl
curl "https://api.telegram.org/bot<TOKEN>/getMe"
```

### Verificar chat ID

```bash
# Enviar mensaje al bot y luego ejecutar
curl "https://api.telegram.org/bot<TOKEN>/getUpdates"
```

### Ejecutar Tests

```bash
# Instalar pytest
pip install pytest

# Ejecutar tests
pytest tests/ -v

# Con coverage
pytest tests/ --cov=. --cov-report=html
```

### Tests Incluidos

| Categoría | Tests |
|-----------|-------|
| Config | ✅ Import, horarios format, mensaje, intervalo |
| Commands | ✅ /start, /stop, /status, /stats |
| Logic | ✅ is_time_to_send, get_uptime |
| Error Handling | ✅ Unknown commands |
| Env Config | ✅ Environment variables |

## 📝 Changelog

### v2.1.0 (2026-03-22)
- ✅ Comandos interactivos (/start, /stop, /status, /stats, /horarios, /ayuda)
- ✅ Sistema de estadísticas integrado
- ✅ Mejor manejo de errores con contadores
- ✅ Integración con python-telegram-bot handlers

### v2.0.0 (2026-03-22)
- ✅ Soporte para múltiples chats (`TELEGRAM_CHAT_IDS`)
- ✅ Mejor manejo de errores y reconexión automática
- ✅ Logging a archivo y consola
- ✅ Manejo graceful de señales (SIGINT/SIGTERM)
- ✅ Validación de configuración al inicio
- ✅ Mensajes con formato Markdown mejorado

### v1.1.0 (2026-03-21)
- ✅ Horarios extendidos hasta medianoche
- ✅ Configuración vía variables de entorno

### v1.0.0 (2026-03-20)
- ✅ Versión inicial con recordatorios básicos

## 📄 Licencia

MIT License - Feel free to use and modify!

## 🤖 Actualizado por

OpenClaw AI Assistant - 2026-03-22
*Mejoras v2.1: Comandos interactivos, estadísticas, mejor manejo de errores*
