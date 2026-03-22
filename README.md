# 🤖 Bot de Hidratación

Bot de Telegram que envía recordatorios de hidratación a lo largo del día.

## 📋 Descripción

Este bot envía mensajes automatizados a intervalos específicos durante el día para recordar hydrate. Fue diseñado para ayudar a mantener una rutina de hidratación saludable.

## 🛠️ Características

- ✅ Recordatorios automáticos cada 1.5 horas
- ✅ Horarios personalizables
- ✅ Mensajes personalizados
- ✅ Modo 24/7
- ✅ Notificación de inicio

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

Crea un archivo `.env` o establece las variables:
```bash
export TELEGRAM_BOT_TOKEN="tu_token_aqui"
export TELEGRAM_CHAT_ID="tu_chat_id_aqui"
```

5. **Ejecutar el bot:**
```bash
python main.py
```

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram | (requerido) |
| `TELEGRAM_CHAT_ID` | ID del chat destino | (requerido) |

### Personalizar Horarios

Edita la lista `HORARIOS` en `main.py`:

```python
HORARIOS = [
    "05:30", "07:00", "08:30", "10:00", "11:30",
    "13:00", "14:30", "16:00", "17:30", "19:00",
    "20:30", "22:00", "23:30", "00:15"
]
```

### Personalizar Mensaje

Edita la variable `MENSAJE` en `main.py`:

```python
MENSAJE = "💧 ¡Hora de tomar agua! Bebe 250 ml y mantente saludable. 🚰💪"
```

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
      - TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
```

## ☁️ Deploy en Render/Railway

1. Conecta tu repositorio a Render o Railway
2. Configura las variables de entorno:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. El comando de inicio: `python main.py`

## 📁 Estructura del Proyecto

```
bot-hidratacion/
├── main.py              # Código principal del bot
├── requirements.txt     # Dependencias Python
├── Procfile            # Para deploy en Railway/Render
├── .env.example        # Ejemplo de configuración
└── README.md           # Este archivo
```

## 🔧 Mantenimiento

### Verificar logs

```bash
# Local
python main.py

# Docker
docker logs -f bot-hidratacion
```

### Reiniciar el bot

Si el bot deja de funcionar, simplemente reinicia el proceso o el contenedor.

## ⚠️ Notas

- El bot funciona continuamente y debe estar siempre activo
- Asegúrate de que el token del bot tenga permisos para enviar mensajes
- El Chat ID debe ser un número (no @username)

## 📝 Historial de Versiones

- **v1.0.0** - Versión inicial con recordatorios básicos
- **v1.1.0** - Horarios extendidos hasta medianoche

## 🔒 Seguridad

- **Token del bot**: Almacenar en variable de entorno, nunca en código
- **Webhooks**: Usar HTTPS en producción
- **Logs**: No registrar información sensible
- **Permisos**: Mínimo privilegio necesario para el bot

## 📄 Licencia

MIT License - Feel free to use and modify!
