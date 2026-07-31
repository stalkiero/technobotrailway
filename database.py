"""
Кожен користувач має власний файл SQLite-бази (data/<user_id>.db),
як вимагає ТЗ ("Окрема база даних для кожного користувача").
"""
import os
import aiosqlite
from datetime import datetime

from config import DB_DIR

os.makedirs(DB_DIR, exist_ok=True)


def _db_path(user_id: int) -> str:
    return os.path.join(DB_DIR, f"{user_id}.db")


async def get_connection(user_id: int) -> aiosqlite.Connection:
    conn = await aiosqlite.connect(_db_path(user_id))
    await conn.execute("PRAGMA journal_mode=WAL;")
    await _ensure_schema(conn)
    return conn


async def _ensure_schema(conn: aiosqlite.Connection) -> None:
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS exits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_key TEXT NOT NULL,
            type_title TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            delayed INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS active_exit (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            type_key TEXT NOT NULL,
            type_title TEXT NOT NULL,
            start_time TEXT NOT NULL,
            planned_minutes INTEGER,
            delayed INTEGER NOT NULL DEFAULT 0,
            chat_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL
        )
        """
    )
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS hour_limit (
            hour_key TEXT PRIMARY KEY,
            count INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    await conn.commit()


# ---------- Активний вихід ----------

async def set_active_exit(conn, type_key, type_title, start_time, planned_minutes, chat_id, message_id):
    await conn.execute("DELETE FROM active_exit")
    await conn.execute(
        """INSERT INTO active_exit (id, type_key, type_title, start_time, planned_minutes,
                                     delayed, chat_id, message_id)
           VALUES (1, ?, ?, ?, ?, 0, ?, ?)""",
        (type_key, type_title, start_time, planned_minutes, chat_id, message_id),
    )
    await conn.commit()


async def get_active_exit(conn):
    cur = await conn.execute("SELECT * FROM active_exit WHERE id = 1")
    row = await cur.fetchone()
    if not row:
        return None
    cols = [d[0] for d in cur.description]
    return dict(zip(cols, row))


async def mark_active_exit_delayed(conn, new_planned_minutes):
    await conn.execute(
        "UPDATE active_exit SET delayed = 1, planned_minutes = ? WHERE id = 1",
        (new_planned_minutes,),
    )
    await conn.commit()


async def clear_active_exit(conn):
    await conn.execute("DELETE FROM active_exit")
    await conn.commit()


# ---------- Журнал виходів ----------

async def add_exit_record(conn, type_key, type_title, start_time, end_time, delayed):
    await conn.execute(
        """INSERT INTO exits (type_key, type_title, start_time, end_time, delayed)
           VALUES (?, ?, ?, ?, ?)""",
        (type_key, type_title, start_time, end_time, int(delayed)),
    )
    await conn.commit()


async def get_all_exits(conn):
    cur = await conn.execute(
        "SELECT type_title, start_time, end_time, delayed FROM exits ORDER BY start_time"
    )
    rows = await cur.fetchall()
    return rows


async def clear_all_exits(conn):
    await conn.execute("DELETE FROM exits")
    await conn.execute("DELETE FROM hour_limit")
    await conn.execute("DELETE FROM active_exit")
    await conn.commit()


# ---------- Обмеження "один вихід на годину" ----------

def hour_key_for(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d-%H")


async def get_hour_count(conn, hour_key: str) -> int:
    cur = await conn.execute("SELECT count FROM hour_limit WHERE hour_key = ?", (hour_key,))
    row = await cur.fetchone()
    return row[0] if row else 0


async def increment_hour_count(conn, hour_key: str) -> None:
    await conn.execute(
        """INSERT INTO hour_limit (hour_key, count) VALUES (?, 1)
           ON CONFLICT(hour_key) DO UPDATE SET count = count + 1""",
        (hour_key,),
    )
    await conn.commit()
