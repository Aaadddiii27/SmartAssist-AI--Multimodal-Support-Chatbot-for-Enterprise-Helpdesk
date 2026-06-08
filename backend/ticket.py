import sqlite3
from datetime import datetime

DB_PATH = "database/smartassist.db"


def create_ticket(issue):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue TEXT,
        status TEXT,
        created_at TEXT
    )
    """)

    cursor.execute("""
    INSERT INTO tickets (
        issue,
        status,
        created_at
    )
    VALUES (?, ?, ?)
    """, (
        issue,
        "Open",
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    ticket_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return ticket_id


def get_tickets():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue TEXT,
        status TEXT,
        created_at TEXT
    )
    """)

    cursor.execute("""
    SELECT *
    FROM tickets
    ORDER BY id DESC
    """)

    tickets = cursor.fetchall()

    conn.close()

    return tickets
def get_open_ticket_count():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM tickets
    WHERE status='Open'
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count