Kontext-Manager

from contextlib import contextmanager
import sqlite3

DB_NAME = "pi_datenbank.db"

@contextmanager
def get_db_connection():
    
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


Tabellen erstellen

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu REAL NOT NULL,
                ram REAL NOT NULL,
                disk REAL NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                component TEXT NOT NULL,
                value REAL NOT NULL
            )
        """)


Stats speichern

def save_stat(timestamp, cpu, ram, disk):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO stats (timestamp, cpu, ram, disk) VALUES (?,?,?,?)",
            (timestamp, cpu, ram, disk)
        )


Warnungen speichern

def save_warning(timestamp, component, value):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO warnings (timestamp, component, value) VALUES (?,?,?)",
            (timestamp, component, value)
        )


Letzte Stats abrufen

def get_recent_stats(limit=10):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, timestamp, cpu, ram, disk FROM stats ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        return cursor.fetchall()
    

Letzte Warnungen abrufen

def get_recent_warnings(limit=10):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, timestamp, component, value FROM warnings ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        return cursor.fetchall()
    

Alle Warnungen abrufen

def get_all_warnings():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, timestamp, component, value FROM warnings ORDER BY timestamp ASC"
        )
        return cursor.fetchall()