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

def save_stat(timestamp, cpu, ram, disk):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO stats (timestamp, cpu, ram, disk) VALUES (?,?,?,?)",
            (timestamp, cpu, ram, disk)
        )

def save_warning(timestamp, component, value):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO warnings (timestamp, component, value) VALUES (?,?,?)",
            (timestamp, component, value)
        )

def get_recent_stats(limit=10):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, timestamp, cpu, ram, disk FROM stats ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        return cursor.fetchall()

def get_recent_warnings(limit=10):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, timestamp, component, value FROM warnings ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        return cursor.fetchall()

# WICHTIG: Erstellt die Tabellen beim ersten Ausführen
if __name__ == "__main__":
    init_db()
    print("Datenbank initialisiert.")