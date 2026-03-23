#!/bin/bash
# Setup script para Bot de Hidratación

set -e

echo "🤖 Configurando Bot de Hidratación..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Instala Python 3.9+"
    exit 1
fi

echo "✅ Python disponible: $(python3 --version)"

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno
echo "📦 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Verificar configuración
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "📝 Copiando .env.example a .env..."
        cp .env.example .env
        echo "⚠️  EDITA .env con tu token de Telegram!"
    else
        echo "⚠️  No hay .env.example"
    fi
else
    echo "✅ Configuración encontrada"
fi

# Verificar token
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    echo "✅ Token de Telegram configurado"
elif grep -q "TELEGRAM_BOT_TOKEN" .env 2>/dev/null; then
    echo "✅ Token configurado en .env"
else
    echo "⚠️  TOKEN NO CONFIGURADO - Edita .env"
fi

# Hacer ejecutable el health check
chmod +x health_check.py

echo ""
echo "✅ Setup completado!"
echo ""
echo "Para iniciar el bot:"
echo "  python3 main.py"
echo ""
echo "Para verificar salud:"
echo "  python3 health_check.py"
echo ""