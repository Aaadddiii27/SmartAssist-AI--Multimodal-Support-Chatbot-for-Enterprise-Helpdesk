import sqlite3
from datetime import datetime

DB_PATH = "database/smartassist.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT,
        bot_response TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_chat(user_message, bot_response):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO chat_history
    (
        user_message,
        bot_response,
        timestamp
    )
    VALUES (?, ?, ?)
    """, (
        user_message,
        bot_response,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()
def get_chat_history(limit=50):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        user_message,
        bot_response,
        timestamp
    FROM chat_history
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))
    cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue TEXT,
    status TEXT,
    created_at TEXT
)
""")
    rows = cursor.fetchall()

    conn.close()

    return rows
def get_total_chats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COUNT(*)
    FROM chat_history
    """)
    total = cursor.fetchone()[0]
    conn.close()
    return total