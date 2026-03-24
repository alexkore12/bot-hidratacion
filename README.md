# 💧 Bot de Hidratación — Tu Asistente Personal de Hidratación

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=flat-square&logo=telegram)
![SQLite](https://img.shields.io/badge/Database-SQLite-green?style=flat-square)
![MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)

Bot de Telegram que combina recordatorios automáticos con registro manual de consumo de agua. Diseñado para ayudarte a mantener una rutina de hidratación saludable con seguimiento de progreso.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Requisitos](#-requisitos)
- [Instalación Rápida](#-instalación-rápida)
- [Comandos](#-comandos)
- [Base de Datos](#-base-de-datos)
- [Configuración](#-configuración)
- [Docker](#-docker)
- [Deployment](#-deployment)
- [Seguridad](#-seguridad)
- [Monitoreo](#-monitoreo)
- [Estructura](#-estructura)
- [Contribución](#-contribución)

---

## ✨ Características

| Categoría | Descripción |
|-----------|-------------|
| **Persistencia SQLite** | Tu historial se guarda localmente |
| **Estadísticas Semanales** | Gráficos de progreso y promedios diarios |
| **Registro Manual** | /log 250, /log 500 cafe con notas |
| **Metas Personalizables** | Cada usuario tiene su propia meta diaria |
| **Historial Completo** | Consulta hasta 30 días de consumo |
| **Comandos Interactivos** | Experiencia tipo aplicación native |
| **Multi-idioma** | Soporte para español e inglés |
| **Notificaciones** | Recordatorios automáticos configurables |
| **Graceful Shutdown** | Cierre limpio sin pérdida de datos |

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                      TELEGRAM                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    USER                                   │    │
│  │  💧 /start  💧 /log 250  💧 /stats  💧 /setgoal 2500    │    │
│  └─────────────────────────────────────────────────────────┘    │
└──────────────────────────────┬──────────────────────────────────┘
                               │ Telegram Bot API
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BOT CORE (Python)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │  Commands    │  │  Reminders   │  │     Database           │  │
│  │  Handler     │──│  Scheduler   │──│    (SQLite)            │  │
│  └──────────────┘  └──────────────┘  └────────────────────────┘  │
│         │                  │                     │                 │
│         ▼                  ▼                     ▼                 │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │  Keyboard    │  │  Message     │  │     Stats              │  │
│  │  Builder     │  │  Formatter   │  │     Calculator         │  │
│  └──────────────┘  └──────────────┘  └────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Requisitos

- **Python**: 3.9 o superior
- **Token de Bot de Telegram**: [Obtener aquí](https://t.me/BotFather)
- **Docker**: Para despliegue en contenedores (opcional)
- **SQLite**: Incluido en Python

---

## 🚀 Instalación Rápida

### Clonar el repositorio

```bash
git clone https://github.com/alexkore12/bot-hidratacion.git
cd bot-hidratacion
```

### Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tu configuración:

```env
TELEGRAM_BOT_TOKEN=tu_token_de_bot_aqui
TELEGRAM_CHAT_IDS=123456789,987654321
REMINDER_INTERVAL=60
DB_PATH=hydration_data.db
LOG_LEVEL=INFO
DEFAULT_GOAL_ML=2000
TIMEZONE=America/Mexico_City
```

### Obtener Token de Telegram

1. Abre Telegram y busca **@BotFather**
2. Envía `/newbot`
3. Sigue las instrucciones y copia el token
4. **[Opcional]** Obtén tu Chat ID con **@userinfobot**

### Ejecutar

```bash
# Modo desarrollo
python main.py

# En background (Linux/Mac)
nohup python main.py > bot.log 2>&1 &

# Con tmux
tmux new -s hydration-bot
python main.py
```

---

## 💬 Comandos

### Comandos Principales

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
| `/resume` | Reanudar recordatorios | `/resume` |

### Ejemplos de Uso

```
/start
→ Bienvenido al Bot de Hidratación 💧
   Tu meta diaria: 2000ml
   Progreso hoy: 0/2000ml (0%)

/log 500
→ ✅ Registrado: 500ml
   Café de la mañana
   Progreso: 500/2000ml (25%)

/log 250 agua con limón
→ ✅ Registrado: 250ml
   agua con limón
   Progreso: 750/2000ml (37%)

/stats
→ 📊 Estadísticas de la semana

   L M M J V S D
   ▓ ▓ ▓ ▓ ▓ ░ ░
   
   Promedio: 1850ml/día
   Meta alcanzada: 4/7 días
   Mejor racha: 5 días

/setgoal 2500
→ 🎯 Meta actualizada a 2500ml/día
```

---

## 🗄️ Base de Datos

### Esquema

El bot usa SQLite para persistir todos los datos localmente:

```sql
-- Archivo: hydration_data.db

-- Tabla: Registro de consumo
CREATE TABLE hydration_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    amount_ml INTEGER NOT NULL,
    note TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    date DATE GENERATED ALWAYS AS (DATE(timestamp)) STORED
);

-- Tabla: Configuración de usuarios
CREATE TABLE user_settings (
    chat_id INTEGER PRIMARY KEY,
    daily_goal_ml INTEGER DEFAULT 2000,
    reminder_interval_minutes INTEGER DEFAULT 60,
    reminder_enabled BOOLEAN DEFAULT 1,
    timezone TEXT DEFAULT 'UTC',
    language TEXT DEFAULT 'es',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: Seguimiento de metas diarias
CREATE TABLE daily_goals (
    date DATE PRIMARY KEY,
    total_ml INTEGER DEFAULT 0,
    goal_ml INTEGER,
    goal_reached BOOLEAN DEFAULT 0
);

-- Tabla: Recordatorios activos
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    hour TIME NOT NULL,
    enabled BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Índices

```sql
CREATE INDEX idx_logs_chat_id ON hydration_logs(chat_id);
CREATE INDEX idx_logs_timestamp ON hydration_logs(timestamp);
CREATE INDEX idx_logs_date ON hydration_logs(date);
```

### Backup y Restore

```bash
# Copia de seguridad
cp hydration_data.db hydration_data_backup_$(date +%Y%m%d).db

# Restaurar
cp hydration_data_backup_20260324.db hydration_data.db

# Ver tamaño
ls -lh hydration_data.db

# Ver uso
sqlite3 hydration_data.db "SELECT COUNT(*) FROM hydration_logs;"
```

---

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram | **Requerido** |
| `TELEGRAM_CHAT_IDS` | IDs de chat separados por coma | **Requerido** |
| `REMINDER_INTERVAL` | Intervalo de verificación (segundos) | `60` |
| `DB_PATH` | Ruta del archivo de base de datos | `hydration_data.db` |
| `LOG_LEVEL` | Nivel de logging | `INFO` |
| `DEFAULT_GOAL_ML` | Meta diaria por defecto | `2000` |
| `TIMEZONE` | Zona horaria | `UTC` |
| `REMINDER_START_HOUR` | Hora inicio recordatorios | `06:00` |
| `REMINDER_END_HOUR` | Hora fin recordatorios | `22:00` |

### Configuración de Horarios

Edita `config.py` para personalizar horarios de recordatorios:

```python
HORARIOS = [
    "06:00", "07:30", "09:00", "10:30",
    "12:00", "13:30", "15:00", "16:30",
    "18:00", "19:30", "21:00", "22:30"
]
```

### Configuración de Mensajes

Edita `config.py` para personalizar mensajes:

```python
MENSAJE_RECORDATORIO = (
    "💧 *¡Hora de hidratarse!*\n\n"
    "Bebe un vaso de agua (250ml)...\n"
    "Tu progreso hoy: {progreso}\n"
    "Te faltan: {restante}ml"
)

MENSAJE_CUMPLIDO = (
    "🎉 *¡Meta diaria alcanzada!*\n\n"
    "Hoy bebiste {total}ml\n"
    "¡Increíble trabajo manteniéndote hidratado!"
)
```

---

## 🐳 Docker

### Build

```bash
docker build -t bot-hidratacion:latest .
```

### Run

```bash
docker run -d \
    --name hydration-bot \
    --env-file .env \
    -v $(pwd)/hydration_data.db:/app/hydration_data.db \
    bot-hidratacion:latest
```

### Docker Compose

```yaml
version: '3.8'

services:
  bot:
    build: .
    env_file: .env
    restart: unless-stopped
    volumes:
      - ./hydration_data.db:/app/hydration_data.db
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Ejecutar

```bash
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## 🚢 Deployment

### Railway (Recomendado)

1. Fork el repositorio
2. Conecta tu cuenta de Railway
3. Selecciona el repositorio
4. Configura las variables de entorno
5. Deploy automático

### Render

```bash
# Usando Procfile
web: python main.py
```

### VPS/Server Propio

```bash
# Instalar
git clone https://github.com/alexkore12/bot-hidratacion.git
cd bot-hidratacion
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar systemd
sudo cp bot-hidratacion.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bot-hidratacion
sudo systemctl start bot-hidratacion

# Ver logs
sudo journalctl -u bot-hidratacion -f
```

### Heroku

```bash
# Login
heroku login

# Create app
heroku create bot-hidratacion

# Set vars
heroku config:set TELEGRAM_BOT_TOKEN=tu_token
heroku config:set TELEGRAM_CHAT_IDS=tu_chat_id

# Deploy
git push heroku main
```

---

## 🔒 Seguridad

| Práctica | Implementación |
|----------|----------------|
| Token en variable de entorno | ✅ Nunca en código |
| Validación de chat IDs | ✅ Solo IDs autorizados |
| Sanitización de input | ✅ En comandos |
| Base de datos local | ✅ Sin datos en la nube |
| Rate limiting | ✅ Implícito en comandos |
| Sin información sensible en logs | ✅ Logs sanitizados |

---

## 📊 Monitoreo

### Ver Logs en Tiempo Real

```bash
# Tail
tail -f bot-hidratacion.log

# Journal (systemd)
sudo journalctl -u bot-hidratacion -f

# Docker
docker-compose logs -f bot
```

### Estado del Proceso

```bash
ps aux | grep "python main.py"
# Output esperado:
# user  12345  0.2  1.2  45678  23456  ?  S  12:00  0:05  python main.py
```

### Métricas de Base de Datos

```bash
# Total de registros
sqlite3 hydration_data.db "SELECT COUNT(*) FROM hydration_logs;"

# Registros de hoy
sqlite3 hydration_data.db "SELECT COUNT(*) FROM hydration_logs WHERE date = DATE('now');"

# Total por usuario
sqlite3 hydration_data.db "SELECT chat_id, COUNT(*) FROM hydration_logs GROUP BY chat_id;"

# Tamaño de DB
ls -lh hydration_data.db
```

### Troubleshooting

| Problema | Solución |
|----------|----------|
| Bot no responde | Verificar token en `.env` |
| Chat ID inválido | Usar @userinfobot para obtener ID numérico |
| Sin recordatorios | Verificar horarios en `HORARIOS` |
| Error de conexión | Revisar logs con `tail -f bot.log` |

---

## 📁 Estructura del Proyecto

```
bot-hidratacion/
├── main.py                  # Punto de entrada v3.0
├── config.py                # Configuración y constantes
├── database.py              # Capa de persistencia SQLite
├── bot_commands.py          # Handlers de comandos interactivos
├── requirements.txt         # Dependencias Python
├── .env.example             # Template de configuración
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Procfile                 # Para Railway/Render
├── deploy.sh                # Script de deployment
├── monitor.sh               # Script de monitoreo
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
└── README.md                # Este archivo
```

---

## 📈 Changelog

### v3.0 (Marzo 2026)

- ✅ Comandos /stop y /resume para pausar recordatorios
- ✅ Soporte multi-idioma (español e inglés)
- ✅ Estadísticas semanales mejoradas
- ✅ Notificaciones de meta alcanzada
- ✅ Historial configurable (1-30 días)
- ✅ Graceful shutdown mejorado

### v2.0

- ✅ Base de datos SQLite para persistencia
- ✅ Comando /stats con estadísticas semanales
- ✅ Comando /log con notas y cantidades personalizadas
- ✅ Comando /setgoal para metas personalizables
- ✅ Comando /history con historial de 30 días
- ✅ Refactorización completa con python-telegram-bot v20

### v1.0

- ✅ Recordatorios automáticos
- ✅ Registro básico de consumo
- ✅ Bot de Telegram funcional

---

## 🤝 Contribución

1. Fork el repositorio
2. Crear branch: `git checkout -b feature/nueva-caracteristica`
3. Commit: `git commit -am 'Agregar nueva característica'`
4. Push: `git push origin feature/nueva-caracteristica'`
5. Crear Pull Request

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

---

## 📚 Recursos

- [Documentación API de Telegram Bots](https://core.telegram.org/bots/api)
- [python-telegram-bot Wiki](https://github.com/python-telegram-bot/python-telegram-bot/wiki)
- [Best Practices for Telegram Bots](https://core.telegram.org/bots/bots-best-practices)
- [Python SQLite Tutorial](https://docs.python.org/3/library/sqlite3.html)

---

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

---

## 👤 Autor

**[@alexkore12](https://github.com/alexkore12)**

---

⭐ **Dale una estrella si te fue útil!**
