# 🤖 Bot de Hidratación

Bot de Telegram que envía recordatorios de hidratación a lo largo del día.

## 📋 Descripción

Este bot envía mensajes automatizados a intervalos específicos durante el día para recordar hidratarse. Fue diseñado para ayudar a mantener una rutina de hidratación saludable.

## 🛠️ Características

- ✅ Recordatorios automáticos cada intervalos personalizados
- ✅ Horarios personalizables
- ✅ Mensajes personalizados con emojis
- ✅ Modo 24/7
- ✅ Notificación de inicio
- ✅ Logging configurable
- ✅ Configuración segura via variables de entorno

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

Copia el archivo de ejemplo y complétalo:
```bash
cp .env.example .env
# Edita .env con tu token y chat_id
```

O establece las variables directamente:
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
| `LOG_LEVEL` | Nivel de logging | INFO |

### Personalizar Horarios

Edita la lista `HORARIOS` en `config.py`:

```python
HORARIOS = [
    "05:30", "07:00", "08:30", "10:00", "11:30",
    "13:00", "14:30", "16:00", "17:30", "19:00",
    "20:30", "22:00", "23:30", "00:15"
]
```

### Personalizar Mensaje

Edita la variable `MENSAJE` en `config.py`:

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
├── config.py            # Configuración centralizada
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

## ⚠️ Notas de Seguridad

- **NUNCA** hardcodes tokens en el código
- Usa siempre variables de entorno en producción
- El archivo `.env` debe estar en `.gitignore`
- Asegúrate de que el token del bot tenga permisos para enviar mensajes

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📝 Historial de Versiones

- **v1.2.0** - Seguridad mejorada con python-dotenv y .env.example
- **v1.1.0** - Horarios extendidos hasta medianoche
- **v1.0.0** - Versión inicial con recordatorios básicos

## 📄 Licencia

MIT License - Siéntete libre de usar y modificar.

---

## 🇬🇧 English Version (README-en.md)

This project also has an English README available in `README-en.md`.
