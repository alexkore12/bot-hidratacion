"""
Database Module - Persistencia SQLite para Bot de Hidratación
Mantiene historial de consumo de agua por usuario/chat
"""
import sqlite3
import os
import logging
from datetime import datetime, date
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# ============================================
# CONFIGURATION
# ============================================

DB_PATH = os.getenv('DB_PATH', 'hydration_data.db')


class HydrationDatabase:
    """Gestión de base de datos SQLite para seguimiento de hidratación"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        """Context manager para conexiones SQLite"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        """Inicializa el esquema de la base de datos"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Tabla de registros de consumo
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hydration_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id TEXT NOT NULL,
                    amount_ml INTEGER NOT NULL DEFAULT 250,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date DATE DEFAULT (DATE('now', 'localtime')),
                    note TEXT
                )
            """)

            # Tabla de configuración por usuario
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    chat_id TEXT PRIMARY KEY,
                    daily_goal_ml INTEGER DEFAULT 2000,
                    reminder_interval INTEGER DEFAULT 5400,
                    notifications_enabled INTEGER DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tabla de metas diarias
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id TEXT NOT NULL,
                    date DATE DEFAULT (DATE('now', 'localtime')),
                    goal_ml INTEGER DEFAULT 2000,
                    achieved INTEGER DEFAULT 0,
                    UNIQUE(chat_id, date)
                )
            """)

            # Índices para consultas rápidas
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_logs_chat_date
                ON hydration_logs(chat_id, date)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_daily_chat_date
                ON daily_goals(chat_id, date)
            """)

            conn.commit()
            logger.info(f"✓ Base de datos inicializada: {self.db_path}")

    # ============================================
    # HYDRATION LOG OPERATIONS
    # ============================================

    def log_water(self, chat_id: str, amount_ml: int = 250, note: str = None) -> Dict[str, Any]:
        """Registra consumo de agua"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO hydration_logs (chat_id, amount_ml, note)
                   VALUES (?, ?, ?)""",
                (str(chat_id), amount_ml, note)
            )
            conn.commit()

            log_id = cursor.lastrowid
            today_total = self.get_today_total(chat_id)

            logger.info(f"💧 [{chat_id}] +{amount_ml}ml logged. Total hoy: {today_total}ml")

            return {
                'id': log_id,
                'chat_id': chat_id,
                'amount_ml': amount_ml,
                'today_total': today_total,
                'goal_ml': self.get_daily_goal(chat_id),
                'progress_pct': min(100, int((today_total / self.get_daily_goal(chat_id)) * 100))
            }

    def get_today_total(self, chat_id: str) -> int:
        """Obtiene el total de agua consumida hoy"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT COALESCE(SUM(amount_ml), 0) as total
                   FROM hydration_logs
                   WHERE chat_id = ? AND date = DATE('now', 'localtime')""",
                (str(chat_id),)
            )
            row = cursor.fetchone()
            return row['total'] if row else 0

    def get_week_stats(self, chat_id: str) -> Dict[str, Any]:
        """Obtiene estadísticas de la semana actual"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """SELECT
                       date,
                       SUM(amount_ml) as daily_total,
                       COUNT(*) as entries
                   FROM hydration_logs
                   WHERE chat_id = ?
                     AND date >= DATE('now', '-7 days', 'localtime')
                   GROUP BY date
                   ORDER BY date""",
                (str(chat_id),)
            )
            days = [dict(row) for row in cursor.fetchall()]

            # Fill missing days with zero
            result = []
            for i in range(7):
                day = (datetime.now().replace(hour=0, minute=0, second=0) -
                       (i * __import__('datetime').timedelta(days=1))).strftime('%Y-%m-%d')
                day_data = next((d for d in days if d['date'] == day), None)
                result.append({
                    'date': day,
                    'total_ml': day_data['daily_total'] if day_data else 0,
                    'entries': day_data['entries'] if day_data else 0
                })

            result.reverse()

            # Calculate averages
            total_ml = sum(d['total_ml'] for d in result)
            avg_daily = total_ml / 7 if total_ml > 0 else 0

            return {
                'days': result,
                'week_total_ml': total_ml,
                'daily_average_ml': round(avg_daily),
                'goal_ml': self.get_daily_goal(chat_id)
            }

    def get_history(self, chat_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """Obtiene historial de consumo"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, amount_ml, timestamp, note
                   FROM hydration_logs
                   WHERE chat_id = ?
                     AND date >= DATE('now', ?, 'localtime')
                   ORDER BY timestamp DESC
                   LIMIT 100""",
                (str(chat_id), f'-{days} days')
            )
            return [dict(row) for row in cursor.fetchall()]

    def reset_daily(self, chat_id: str) -> bool:
        """Resetea el contador diario (acción administrativa)"""
        # No eliminamos datos históricos, solo marcamos
        logger.info(f"🔄 Reset solicitado para {chat_id}")
        return True

    # ============================================
    # USER SETTINGS
    # ============================================

    def get_daily_goal(self, chat_id: str) -> int:
        """Obtiene la meta diaria de agua para un chat"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT daily_goal_ml FROM user_settings WHERE chat_id = ?",
                (str(chat_id),)
            )
            row = cursor.fetchone()
            return row['daily_goal_ml'] if row else 2000

    def set_daily_goal(self, chat_id: str, goal_ml: int) -> bool:
        """Configura la meta diaria de agua"""
        if not (500 <= goal_ml <= 5000):
            return False

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO user_settings (chat_id, daily_goal_ml, updated_at)
                   VALUES (?, ?, CURRENT_TIMESTAMP)
                   ON CONFLICT(chat_id)
                   DO UPDATE SET daily_goal_ml = ?, updated_at = CURRENT_TIMESTAMP""",
                (str(chat_id), goal_ml, goal_ml)
            )
            conn.commit()
            logger.info(f"🎯 [{chat_id}] Meta diaria actualizada: {goal_ml}ml")
            return True

    def get_all_chat_ids(self) -> List[str]:
        """Obtiene todos los chat IDs que han usado el bot"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT chat_id FROM hydration_logs")
            return [row['chat_id'] for row in cursor.fetchall()]

    # ============================================
    # DAILY GOALS TRACKING
    # ============================================

    def check_daily_goal(self, chat_id: str) -> Dict[str, Any]:
        """Verifica si se alcanzó la meta diaria"""
        today = date.today().isoformat()
        goal = self.get_daily_goal(chat_id)
        total = self.get_today_total(chat_id)

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Upsert daily goal record
            cursor.execute(
                """INSERT INTO daily_goals (chat_id, date, goal_ml, achieved)
                   VALUES (?, ?, ?, ?)
                   ON CONFLICT(chat_id, date)
                   DO UPDATE SET
                       goal_ml = excluded.goal_ml,
                       achieved = CASE WHEN ? >= goal_ml THEN 1 ELSE 0 END""",
                (str(chat_id), today, goal, 1 if total >= goal else 0, total)
            )
            conn.commit()

        return {
            'date': today,
            'total_ml': total,
            'goal_ml': goal,
            'achieved': total >= goal,
            'remaining_ml': max(0, goal - total)
        }


# Instancia global de la base de datos
db = HydrationDatabase()


def get_db() -> HydrationDatabase:
    """Retorna la instancia de base de datos"""
    return db
