"""
Database setup and initialization for the app.
"""

from pathlib import Path
import sqlite3

# Base directory and data folder
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"


def get_db() -> sqlite3.Connection:
    """
    Get a SQLite database connection. Ensures the data directory exists
    and initializes the database tables if they don't exist.
    """
    # Create data directory if it doesn't exist
    DATA_DIR.mkdir(exist_ok=True)

    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable dict-like row access

    # Initialize tables if not already present
    _init(conn)
    return conn


def _init(conn: sqlite3.Connection):
    """
    Initialize the database tables for users and classes.
    """
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'student')),
            salt BLOB NOT NULL,
            pwhash BLOB NOT NULL
        )
    """)

    # Classes table
    c.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            teacher TEXT,
            code TEXT,
            house TEXT,
            notes TEXT
        )
    """)

    conn.commit()


def seed_classes_if_empty():
    """
    Seed the classes table with default data if it is empty.
    """
    conn = get_db()
    cur = conn.cursor()

    # Check if there are already classes
    cur.execute("SELECT COUNT(*) FROM classes")
    count = cur.fetchone()[0]

    if count == 0:
        # Insert default classes
        cur.executemany("""
            INSERT INTO classes (title, teacher, code, house, notes)
            VALUES (?, ?, ?, ?, ?)
        """, [
            ("Calculus", "Ms. Lee", "H2", "Hillary", "Bring calculator"),
            ("Business Studies", "Mrs. Jones", "M5", "Mansfield", "Internal due Friday"),
            ("DDT", "Ms. Bharani", "L4", "Rutherford", "Project work"),
            ("Physics", "Mr. Chang", "T4", "Te Kanawa", "Internal due Thursday"),
            ("English", "Mrs. Knibbs", "B5", "Batten", "Internal due Monday")
        ])
        conn.commit()
