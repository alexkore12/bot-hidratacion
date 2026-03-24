"""
Bot Commands - Handlers para comandos interactivos del Bot de Hidratación
Maneja /log, /stats, /reset, /setgoal, /history, /help, /start, /status, /stop
"""
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from database import get_db
from config import HORARIOS

logger = logging.getLogger(__name__)

# ============================================
# COMMAND HANDLERS
# ============================================


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja /start - Mensaje de bienvenida"""
    chat_id = str(update.effective_chat.id)
    db = get_db()

    goal = db.get_daily_goal(chat_id)
    today = db.get_today_total(chat_id)

    welcome = (
        "👋 *¡Bienvenido al Bot de Hidratación!*\n\n"
        "Soy tu asistente personal para mantenerte hidratado durante el día. "
        "Aquí tienes todo lo que puedes hacer:\n\n"
        "💧 *Registrar agua:* `/log` o `/log 500`\n"
        "📊 *Ver estadísticas:* `/stats`\n"
        "🎯 *Cambiar meta:* `/setgoal 2500`\n"
        "📜 *Ver historial:* `/history`\n"
        "ℹ️ *Ayuda:* `/help`\n\n"
        f"📅 *Tu meta diaria:* {goal}ml\n"
        f"💧 *Hoy llevas:* {today}ml\n\n"
        "¡Empieza a registrar tu consumo de agua!"
    )

    await update.message.reply_text(welcome, parse_mode='Markdown')


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja /help - Guía de comandos"""
    help_text = (
        "📚 *Guía de Comandos*\n\n"
        "━━━━━━━ *Registro* ━━━━━━━\n"
        "`/log` - Registra 250ml (1 vaso)\n"
        "`/log 500` - Registra cantidad personalizada\n"
        "`/log 250 cafe` - Registra con nota\n\n"
        "━━━━━━ *Estadísticas* ━━━━━━\n"
        "`/stats` - Tu progreso semanal\n"
        "`/stats mensual` - Resumen del mes\n\n"
        "━━━━━━ *Configuración* ━━━━━━\n"
        "`/setgoal 2000` - Cambia tu meta diaria (ml)\n"
        "`/status` - Estado actual del bot\n"
        "`/history` - Ver últimas entradas\n\n"
        "━━━━━━ *Control* ━━━━━━━━━━\n"
        "`/start` - Reiniciar bot\n"
        "`/stop` - Detener recordatorios\n"
        "`/reset` - Resetear contador diario\n\n"
        "━━━━━━━ *Horarios* ━━━━━━━━━\n"
        f"Recordatorios activos: *{', '.join(HORARIOS)}*\n\n"
        "💡 *Tip:* Los recordatorios automáticos se envían "
        "en los horarios configurados. ¡Pero puedes registrar "
        "agua manualmente en cualquier momento!"
    )

    await update.message.reply_text(help_text, parse_mode='Markdown')


async def cmd_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja /log - Registrar consumo de agua"""
    chat_id = str(update.effective_chat.id)
    db = get_db()

    # Parsear cantidad y nota
    amount = 250  # default
    note = None

    if context.args:
        # Primer argumento: cantidad
        try:
            amount = int(context.args[0])
            if amount < 10 or amount > 2000:
                await update.message.reply_text(
                    "⚠️ Cantidad inválida. Use entre 10ml y 2000ml.\n"
                    "Ejemplo: `/log 500`"
                )
                return
        except ValueError:
            await update.message.reply_text(
                "⚠️ Cantidad inválida. Use `/log 250` o `/log 500 cafe`"
            )
            return

        # Segundo argumento (opcional): nota
        if len(context.args) > 1:
            note = ' '.join(context.args[1:])[:100]

    # Registrar en base de datos
    result = db.log_water(chat_id, amount, note)
    goal = result['goal_ml']
    total = result['today_total']
    progress = result['progress_pct']

    # Barra de progreso visual
    filled = '🟦' * (progress // 10)
    empty = '⬜' * (10 - (progress // 10))
    bar = filled + empty

    emoji = "🎉" if result['achieved'] else "💧"

    message = (
        f"{emoji} *¡Agua registrada!*\n\n"
        f"➕ *+{amount}ml*"
    )
    if note:
        message += f" ({note})"

    message += (
        f"\n\n"
        f"📊 *Progreso de hoy:*\n"
        f"{bar} {progress}%\n"
        f"💧 {total}ml / {goal}ml\n"
    )

    if total >= goal:
        message += "\n✅ *¡Meta diaria alcanzada!* ¡Excelente!"
    else:
        remaining = goal - total
        message += f"\n📍 Faltan {remaining}ml para tu meta"

    await update.message.reply_text(message, parse_mode='Markdown')


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja /stats - Estadísticas semanales"""
    chat_id = str(update.effective_chat.id)
    db = get_db()

    stats = db.get_week_stats(chat_id)
    goal = stats['goal_ml']
    week_total = stats['week_total_ml']
    daily_avg = stats['daily_average_ml']

    # Build stats message
    lines = ["📊 *Estadísticas Semanales*\n"]

    for day in stats['days']:
        date_str = day['date']
        day_label = datetime.strptime(date_str, '%Y-%m-%d').strftime('%a')
        total = day['total_ml']

        if total >= goal:
            icon = "✅"
        elif total > 0:
            icon = "💧"
        else:
            icon = "⚪"

        pct = min(100, int((total / goal) * 100)) if goal > 0 else 0
        lines.append(f"{icon} {day_label}: {total}ml ({pct}%)")

    lines.append(f"\n📈 *Resumen:*")
    lines.append(f"• Total semana: {week_total}ml")
    lines.append(f"• Promedio diario: {daily_avg}ml")
    lines.append(f"• Meta diaria: {goal}ml")

    if daily_avg >= goal:
        days_above = sum(1 for d in stats['days'] if d['total_ml'] >= goal)
        lines.append(f"\n🌟 ¡{days_above}/7 días alcanzaste tu meta!")
    elif daily_avg > 0:
        deficit = goal - daily_avg
        lines.append(f"\n📍 {deficit}ml debajo de tu meta por día")

    await update.message.reply_text('\n'.join(lines), parse_mode='Markdown')


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja /status - Estado actual"""
    chat_id = str(update.effective_chat.id)
    db = get_db()

    goal = db.get_daily_goal(chat_id)
    total = db.get_today_total(chat_id)
    progress = min(100, int((total / goal) * 100)) if goal > 0 else 0

    filled = '🟦' * (progress // 10)
    empty = '⬜' * (10 - (progress // 10))
    bar = filled + empty

    now = datetime.now().strftime('%H:%M')
    next_reminder = None
    for h in HORARIOS:
        if h > now:
            next_reminder = h
            break

    status = (
        f"📋 *Estado del Bot*\n\n"
        f"🆔 Chat ID: `{chat_id}`\n"
        f"⏰ Hora actual: {now}\n\n"
        f"{bar} {progress}%\n"
        f"💧 {total}ml / {goal}ml\n\n"
        f"🎯 Meta diaria: {goal}ml\n"
    )

    if next_reminder:
        status += f"🔔 Próximo recordatorio: {next_reminder}\n"
    else:
        status += f"🔔 Último recordatorio del día ya pasó\n"

    status += f"📜 Horarios activos: {len(HORARIOS)}\n\n"
    status += f"✅ Bot funcionando correctamente"

    await update.message.reply_text(status, parse_mode='Markdown')


async def cmd_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja /stop - Detener recordatorios"""
    await update.message.reply_text(
        "⏸️ *Recordatorios pausados*\n\n"
        "Los recordatorios automáticos se han detenido. "
        "Usa `/start` para reanudarlos.\n\n"
        "Tu historial de hidratación se mantiene guardado.",
        parse_mode='Markdown'
    )


async def cmd_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja /reset - Confirmación de reset"""
    # El reset real no borra datos (por seguridad)
    # Solo muestra el estado actual

    chat_id = str(update.effective_chat.id)
    db = get_db()

    total = db.get_today_total(chat_id)
    goal = db.get_daily_goal(chat_id)

    await update.message.reply_text(
        "🔄 *Función de Reset*\n\n"
        "El contador diario se resetea automáticamente a medianoche.\n"
        "Los datos históricos se preservan para tus estadísticas.\n\n"
        f"📊 Tu progreso hoy: {total}ml / {goal}ml",
        parse_mode='Markdown'
    )


async def cmd_setgoal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja /setgoal - Cambiar meta diaria"""
    if not context.args:
        chat_id = str(update.effective_chat.id)
        db = get_db()
        current = db.get_daily_goal(chat_id)
        await update.message.reply_text(
            f"🎯 *Meta diaria actual:* {current}ml\n\n"
            "Usa `/setgoal 2000` para cambiarla.\n"
            "Rango válido: 500ml - 5000ml",
            parse_mode='Markdown'
        )
        return

    try:
        new_goal = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "⚠️ Cantidad inválida. Usa `/setgoal 2500`"
        )
        return

    if new_goal < 500 or new_goal > 5000:
        await update.message.reply_text(
            "⚠️ La meta debe estar entre 500ml y 5000ml"
        )
        return

    chat_id = str(update.effective_chat.id)
    db = get_db()

    if db.set_daily_goal(chat_id, new_goal):
        await update.message.reply_text(
            f"✅ *Meta actualizada*\n\n"
            f"🎯 Nueva meta diaria: {new_goal}ml",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "⚠️ No se pudo actualizar la meta. Intenta de nuevo."
        )


async def cmd_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja /history - Ver historial reciente"""
    chat_id = str(update.effective_chat.id)
    db = get_db()

    days = 7
    if context.args and context.args[0].isdigit():
        days = min(30, int(context.args[0]))

    history = db.get_history(chat_id, days)

    if not history:
        await update.message.reply_text(
            "📭 *Sin historial*\n\n"
            "Aún no has registrado agua. ¡Usa `/log` para empezar!"
        )
        return

    lines = [f"📜 *Historial (últimos {days} días)*\n"]

    current_date = None
    for entry in history[:15]:  # Limit to 15 entries
        dt = datetime.fromisoformat(entry['timestamp'])
        date_str = dt.strftime('%Y-%m-%d')

        if date_str != current_date:
            lines.append(f"\n📅 {date_str}")
            current_date = date_str

        time_str = dt.strftime('%H:%M')
        note_str = f" ({entry['note']})" if entry['note'] else ""
        lines.append(f"  🕐 {time_str} • {entry['amount_ml']}ml{note_str}")

    if len(history) > 15:
        lines.append(f"\n... y {len(history) - 15} entradas más")

    await update.message.reply_text('\n'.join(lines), parse_mode='Markdown')


# ============================================
# COMMAND REGISTRY
# ============================================

COMMAND_HANDLERS = {
    'start': cmd_start,
    'help': cmd_help,
    'log': cmd_log,
    'stats': cmd_stats,
    'status': cmd_status,
    'stop': cmd_stop,
    'reset': cmd_reset,
    'setgoal': cmd_setgoal,
    'history': cmd_history,
}


def get_all_commands() -> dict:
    """Retorna la lista de comandos para registro con BotFather"""
    return {
        'start': 'Iniciar el bot y mostrar bienvenida',
        'help': 'Mostrar guía de comandos',
        'log': 'Registrar consumo de agua (ej: /log 250)',
        'stats': 'Ver estadísticas semanales',
        'status': 'Ver estado actual del bot',
        'stop': 'Detener recordatorios',
        'reset': 'Información sobre reset',
        'setgoal': 'Cambiar meta diaria (ej: /setgoal 2000)',
        'history': 'Ver historial de consumo',
    }
