# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al Bot de Hidratación! 🎉

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Reportar Bugs](#reportar-bugs)
- [Solicitar Features](#solicitar-features)

## Código de Conducta

Este proyecto adheres a un código de conducta. Al participar, te comprometes a mantener un ambiente respetuoso.

## Cómo Contribuir

### Tipos de Contribuciones

- 🐛 **Bug Reports** - Reportar errores
- 💡 **Feature Requests** - Sugerir nuevas características
- 📖 **Documentation** - Mejorar documentación
- 🔧 **Code** - Enviar patches/código
- 🌍 **Translations** - Traducciones

### Pasos para Contribuir

1. **Fork el repositorio**
2. **Clona tu fork:**
   ```bash
   git clone https://github.com/tu-usuario/bot-hidratacion.git
   cd bot-hidratacion
   ```
3. **Crea un branch:**
   ```bash
   git checkout -b feature/nueva-caracteristica
   # o
   git checkout -b fix/correccion-bug
   ```
4. **Instala dependencias:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install pytest pytest-asyncio
   ```
5. **Haz tus cambios**
6. **Ejecuta tests:**
   ```bash
   pytest tests/
   ```
7. **Commit:**
   ```bash
   git commit -m "feat: agregar nueva característica"
   ```
8. **Push:**
   ```bash
   git push origin feature/nueva-caracteristica
   ```
9. **Abre un Pull Request**

## Proceso de Desarrollo

### Setup Local

```bash
# Clonar repo
git clone https://github.com/alexkore12/bot-hidratacion.git
cd bot-hidratacion

# Crear venv
python3 -m venv venv
source venv/bin/activate

# Instalar deps de desarrollo
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Configurar pre-commit hooks (opcional)
pre-commit install
```

### Testing

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=src --cov-report=html

# Tests específicos
pytest tests/test_reminders.py -v
```

### Formato de Commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: nueva característica
fix: corrección de bug
docs: cambios en documentación
style: formato, sin cambio de código
refactor: refactorización
test: agregar tests
chore: mantenimiento
```

### Ramas

- `main` - Código en producción
- `develop` - Desarrollo activo
- `feature/*` - Nuevas características
- `fix/*` - Correcciones
- `hotfix/*` - Correcciones urgentes

## Estándares de Código

### Python

- Follow [PEP 8](https://pep8.org/)
- Máximo 120 caracteres por línea
- Usar type hints donde sea posible
- Docstrings en formato Google

```python
def send_reminder(chat_id: int, message: str) -> bool:
    """Envía un recordatorio a un chat específico.
    
    Args:
        chat_id: ID del chat de Telegram
        message: Mensaje a enviar
        
    Returns:
        True si se envió exitosamente, False en caso contrario
    """
    pass
```

### Code Review

- Todo PR requiere al menos 1 aprobación
- Tests deben pasar
- No hay conflictos con main
- Documentación actualizada

## Reportar Bugs

### Formato de Bug Report

```markdown
**Descripción del Bug**
Descripción clara y concisa.

**Pasos para Reproducir**
1. Ve a '...'
2. Haz clic en '...'
3. Ejecuta '...'
4. Ver error

**Comportamiento Esperado**
Lo que debería pasar.

**Comportamiento Actual**
Lo que pasa actualmente.

**Logs/Screenshots**
Si aplica.

**Ambiente:**
- OS: [ej. Ubuntu 22.04]
- Python: [ej. 3.10]
- Versión del bot: [ej. 2.0]
```

## Solicitar Features

### Formato de Feature Request

```markdown
**Problema/ Necesidad**
Descripción clara del problema o necesidad.

**Solución Propuesta**
Tu idea para resolverlo.

**Alternativas Consideradas**
Otras soluciones que consideraste.

**Contexto Adicional**
Screenshots, ejemplos, etc.
```

## 📧 Contacto

Para preguntas, abre un issue o contacta al maintainer.

---

¡Gracias por contribuir! 🙏
