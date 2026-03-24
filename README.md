# 🤖 Bot de Hidratación

> Tu asistente personal de hidratación - nunca más olvides beber agua 💧

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Telegram Bot](https://img.shields.io/badge/Telegram%20Bot-API-blue.svg)](https://core.telegram.org/bots/api)

## 📋 Descripción

Bot de Telegram que envía recordatorios de hidratación a lo largo del día. Diseñado para ayudar a mantener una rutina de hidratación saludable con mensajes personalizados y statistics de seguimiento.

## ✨ Características

- ✅ **Recordatorios Configurables** - Intervalo personalizable (default: cada 1.5 horas)
- ✅ **Soporte Multi-Chat** - Envía recordatorios a múltiples chats simultaneamente
- ✅ **Mensajes Personalizados** - Mensajes motivacionales con soporte Markdown
- ✅ **Modo 24/7** - Auto-reconexión automática ante desconexiones
- ✅ **Logging Completo** - Registros detallados en archivo y consola
- ✅ **Graceful Shutdown** - Manejo correcto de señales SIGINT/SIGTERM
- ✅ **Notificaciones de Horario** - Indica horarios activos de hidratación
- ✅ **Estadísticas** - Historial de hidratación (próximamente)

## 🚀 Instalación

### Prerrequisitos

- Python 3.9 o superior
- Token de Bot de Telegram ([obtener aquí](https://t.me/BotFather))

### Pasos de Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/alexkore12/bot-hidratacion.git
cd bot-hidratacion
```

2. **Crear entorno virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
cp .env.example .env
```

Edita `.env` con tu configuración:
```env
TELEGRAM_BOT_TOKEN=tu_token_aqui
CHAT_IDS=123456789,987654321
REMINDER_INTERVAL=5400  # segundos (1.5 horas)
WATER_GOAL=2000  # ml diarios
TIMEZONE=America/Mexico_City
LOG_LEVEL=INFO
```

5. **Ejecutar el bot:**
```bash
# Desarrollo
python main.py

# Producción (con screen/tmux)
python main.py &
```

### Docker

```bash
# Construir imagen
docker build -t bot-hidratacion .

# Ejecutar
docker run -d --env-file .env bot-hidratacion
```

### Docker Compose

```bash
docker-compose up -d
```

## 📖 Uso

### Comandos del Bot

| Comando | Descripción |
|---------|-------------|
| `/start` | Inicia el bot y muestra mensaje de bienvenida |
| `/help` | Muestra información de ayuda |
| `/status` | Muestra el estado actual del bot |
| `/setinterval <minutos>` | Cambia el intervalo de recordatorios |
| `/stop` | Detiene los recordatorios |
| `/stats` | Muestra estadísticas de hidratación |

### Ejemplo de Mensaje

```
💧 ¡Hora de hidratarte!
Meta: 2000ml | Actual: 1200ml
Próximo recordatorio: 14:30
```

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Token de tu bot de Telegram | **Requerido** |
| `CHAT_IDS` | IDs de chat separados por coma | **Requerido** |
| `REMINDER_INTERVAL` | Intervalo en segundos | `5400` (1.5h) |
| `WATER_GOAL` | Meta diaria de agua en ml | `2000` |
| `TIMEZONE` | Zona horaria | `America/Mexico_City` |
| `LOG_LEVEL` | Nivel de logging | `INFO` |

### Mensajes Personalizados

Edita `config.py` para personalizar los mensajes:

```python
REMINDER_MESSAGES = [
    "💧 ¡Hora de hidratarte! Un vaso de agua te espera.",
    "🌊 Recordatorio: Tu cuerpo necesita agua. ¡Bebe!",
    "💙 Mantente hidratado. Toma un descanso y bebe agua.",
]
```

## 🏗️ Estructura del Proyecto

```
bot-hidratacion/
├── main.py           # Punto de entrada principal
├── config.py         # Configuración del bot
├── requirements.txt  # Dependencias Python
├── .env.example     # Template de variables de entorno
├── deploy.sh        # Script de deployment
├── monitor.sh       # Script de monitoreo
├── SECURITY.md      # Política de seguridad
├── CODE_OF_CONDUCT.md
├── LICENSE
└── README.md
```

## 🔒 Seguridad

- ✅ Token del bot en variable de entorno (nunca en código)
- ✅ Validación de chat IDs autorizados
- ✅ Rate limiting en mensajes
- ✅ Sin datos personales almacenados
- ✅ Logs sin información sensible

Ver [SECURITY.md](SECURITY.md) para más detalles.

## 📊 Monitoreo

```bash
# Ver logs en tiempo real
tail -f hydration_bot.log

# Ver estado del proceso
ps aux | grep bot-hidratacion

# Reiniciar servicio
./deploy.sh
```

## 🐳 Docker

```bash
# Construir
docker build -t bot-hidratacion:latest .

# Ejecutar en background
docker run -d --name hydration-bot \
  --env-file .env \
  bot-hidratacion:latest

# Ver logs
docker logs -f hydration-bot

# Detener
docker stop hydration-bot && docker rm hydration-bot
```

## 🤝 Contribuir

1. Fork el repositorio
2. Crear branch: `git checkout -b feature/nueva-caracteristica`
3. Commit: `git commit -am 'Agregar nueva característica'`
4. Push: `git push origin feature/nueva-caracteristica`
5. Crear Pull Request

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

## 📝 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## 🔗 Enlaces Útiles

- [Documentación API de Telegram Bots](https://core.telegram.org/bots/api)
- [python-telegram-bot Wiki](https://github.com/python-telegram-bot/python-telegram-bot/wiki)
- [Best Practices for Telegram Bots](https://core.telegram.org/bots/bots-best-practices)
