# 💧 Bot de Hidratación

> Tu asistente personal de hidratación — nunca más olvides beber agua.
> Registro de consumo, estadísticas semanales y recordatorios automáticos.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-v20-green.svg)](https://github.com/python-telegram-bot/python-telegram-bot)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![SQLite](https://img.shields.io/badge/Database-SQLite-orange.svg)](https://sqlite.org)

## ✨ Lo Nuevo en v3.0

- 🗄️ **Persistencia SQLite** — Tu historial de hidratación se guarda para siempre
- 📊 **Estadísticas semanales** — Gráficos de progreso y promedios diarios
- 📝 **Registro manual** — `/log 250`, `/log 500 cafe` con notas
- 🎯 **Metas personalizables** — Cada usuario tiene su propia meta diaria
- 📜 **Historial completo** — Consulta hasta 30 días de consumo
- ⚡ **Comandos interactivos** — Experiencia tipo aplicación native

## 📋 Descripción

Bot de Telegram que combina **recordatorios automáticos** con **registro manual** de consumo de agua. Diseñado para ayudarte a mantener una rutina de hidratación saludable con seguimiento de progreso.

## 🚀 Instalación

### Prerrequisitos

- Python 3.9 o superior
- Token de Bot de Telegram ([obtener aquí](https://t.me/BotFather))
- Opcional: Docker para despliegue en contenedores

### Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/alexkore12/bot-hidratacion.git
cd bot-hidratacion

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
```

Edita `.env` con tu configuración:

```env
TELEGRAM_BOT_TOKEN=tu_token_de_bot_aqui
TELEGRAM_CHAT_IDS=123456789,987654321
REMINDER_INTERVAL=60
DB_PATH=hydration_data.db
LOG_LEVEL=INFO
```

### Ejecución

```bash
# Modo desarrollo
python main.py

# En background (Linux/Mac)
nohup python main.py > bot.log 2>&1 &

# Con tmux
tmux new -s hydration-bot
python main.py
```

### Docker

```bash
# Construir imagen
docker build -t bot-hidratacion .

# Ejecutar
docker run -d \
  --name hydration-bot \
  --env-file .env \
  bot-hidratacion
```

### Docker Compose

```yaml
services:
  bot:
    build: .
    env_file: .env
    restart: unless-stopped
    volumes:
      - ./hydration_data.db:/app/hydration_data.db
```

## 📖 Comandos del Bot

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/start` | Iniciar bot y mostrar bienvenida | `/start` |
| `/help` | Guía completa de comandos | `/help` |
| `/log` | Registrar 250ml de agua | `/log` |
| `/log 500` | Registrar cantidad personalizada | `/log 500` |
| `/log 250 cafe` | Registrar con nota | `/log 250 cafe` |
| `/stats` | Estadísticas de la semana | `/stats` |
| `/status` | Progreso actual del día | `/status` |
| `/setgoal 2500` | Cambiar meta diaria (ml) | `/setgoal 2500` |
| `/history` | Últimos registros | `/history` |
| `/history 14` | Historial de 14 días | `/history 14` |
| `/stop` | Detener recordatorios | `/stop` |

## 🗄️ Base de Datos

El bot usa **SQLite** para persistir todos los datos localmente:

```
hydration_data.db
```

### Esquema

- `hydration_logs` — Registro de cada consumo (chat_id, cantidad, timestamp, nota)
- `user_settings` — Configuración por usuario (meta diaria, intervalo)
- `daily_goals` — Seguimiento de metas diarias

### Backup

```bash
# Copia de seguridad
cp hydration_data.db hydration_data_backup_$(date +%Y%m%d).db

# Restaurar
cp hydration_data_backup_20260324.db hydration_data.db
```

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram | **Requerido** |
| `TELEGRAM_CHAT_IDS` | IDs de chat separados por coma | **Requerido** |
| `REMINDER_INTERVAL` | Intervalo de verificación (segundos) | `60` |
| `DB_PATH` | Ruta del archivo de base de datos | `hydration_data.db` |
| `LOG_LEVEL` | Nivel de logging | `INFO` |

### Horarios de Recordatorios

Edita `config.py` para personalizar horarios:

```python
HORARIOS = [
    "06:00", "07:30", "09:00", "10:30",
    "12:00", "13:30", "15:00", "16:30",
    "18:00", "19:30", "21:00", "22:30"
]
```

### Mensajes Personalizados

Edita `config.py` para personalizar los mensajes:

```python
MENSAJE = (
    "💧 *¡Hora de hidratarse!*\n\n"
    "Bebe un vaso de agua (250ml)...\n"
)
```

## 🏗️ Estructura del Proyecto

```
bot-hidratacion/
├── main.py            # Punto de entrada v3.0
├── config.py          # Configuración y constantes
├── database.py        # Capa de persistencia SQLite
├── bot_commands.py    # Handlers de comandos interactivos
├── requirements.txt   # Dependencias Python
├── .env.example      # Template de configuración
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Procfile          # Para deployment en Railway/Render
├── deploy.sh         # Script de deployment
├── monitor.sh        # Script de monitoreo
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── README.md
```

## 🔒 Seguridad

- ✅ Token del bot en variable de entorno (nunca en código)
- ✅ Validación de chat IDs autorizados
- ✅ Sanitización de input en comandos
- ✅ Base de datos local (sin datos en la nube)
- ✅ Rate limiting implícito en comandos
- ✅ Sin información sensible en logs

Ver [SECURITY.md](SECURITY.md) para detalles completos.

## 📊 Monitoreo

```bash
# Ver logs en tiempo real
tail -f bot-hidratacion.log

# Ver estado del proceso
ps aux | grep "python main.py"

# Ver uso de base de datos
sqlite3 hydration_data.db "SELECT COUNT(*) FROM hydration_logs;"

# Ver tamaño de DB
ls -lh hydration_data.db
```

## 🔧 Troubleshooting

### Error: "No se especificó TELEGRAM_BOT_TOKEN"
 Asegúrate de que `.env` existe y contiene el token válido.

### Error: "Chat ID no válido"
 Verifica que el `TELEGRAM_CHAT_ID` es numérico (no @username).

### El bot no responde a comandos
 Verifica que pusiste el bot en el grupo con permisos de lectura.

### Recordatorios no se envían
 Revisa que los horarios en `HORARIOS` cubren la hora actual.

## 🤝 Contribuir

1. Fork el repositorio
2. Crear branch: `git checkout -b feature/nueva-caracteristica`
3. Commit: `git commit -am 'Agregar nueva característica'`
4. Push: `git push origin feature/nueva-caracteristica`
5. Crear Pull Request

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

## 📝 Changelog

### v3.0 (2026-03-24)
- 🗄️ Base de datos SQLite para persistencia
- 📊 Comando `/stats` con estadísticas semanales
- 📝 Comando `/log` con notas y cantidades personalizadas
- 🎯 Comando `/setgoal` para metas personalizables
- 📜 Comando `/history` con historial de 30 días
- ⚡ Refactorización completa con python-telegram-bot v20
- 🐛 Bugfixes y manejo de errores mejorado

### v2.0
- Soporte multi-chat
- Logging mejorado
- Graceful shutdown

### v1.0
- Versión inicial con recordatorios básicos

## 📝 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## 🔗 Enlaces Útiles

- [Documentación API de Telegram Bots](https://core.telegram.org/bots/api)
- [python-telegram-bot Wiki](https://github.com/python-telegram-bot/python-telegram-bot/wiki)
- [Best Practices for Telegram Bots](https://core.telegram.org/bots/bots-best-practices)
- [Python SQLite Tutorial](https://docs.python.org/3/library/sqlite3.html)
