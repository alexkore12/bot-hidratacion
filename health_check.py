#!/usr/bin/env python3
"""
Health Check para Bot de Hidratación
Verifica que el bot esté funcionando correctamente
"""

import os
import sys
import subprocess
import requests
from datetime import datetime


def check_process():
    """Verificar que el proceso del bot esté corriendo"""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "python.*main.py"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False


def check_log():
    """Verificar que el log no tenga errores recientes"""
    log_file = "bot-hidratacion.log"
    if not os.path.exists(log_file):
        return True  # No log file is OK
    
    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
            recent_lines = lines[-20:] if len(lines) > 20 else lines
            
        # Check for ERROR or FATAL in last hour
        for line in recent_lines:
            if "ERROR" in line or "FATAL" in line:
                return False
        return True
    except Exception:
        return False


def check_telegram():
    """Verificar conectividad con Telegram API"""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        return None  # Unknown
    
    try:
        response = requests.get(
            f"https://api.telegram.org/bot{token}/getMe",
            timeout=5
        )
        return response.ok
    except Exception:
        return False


def main():
    """Ejecutar todos los checks"""
    print(f"🔍 Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    checks = {
        "Process": check_process(),
        "Log Errors": check_log(),
        "Telegram API": check_telegram()
    }
    
    all_passed = True
    for name, result in checks.items():
        status = "✅ OK" if result else "❌ FAIL"
        print(f"{name}: {status}")
        if result is False:
            all_passed = False
    
    print("-" * 50)
    if all_passed:
        print("✅ Bot saludable")
        sys.exit(0)
    else:
        print("❌ Problemas detectados")
        sys.exit(1)


if __name__ == "__main__":
    main()