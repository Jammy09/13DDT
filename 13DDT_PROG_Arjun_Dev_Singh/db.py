
from pathlib import Path
import sqlite3
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"

def get_db():
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    _init(conn)
    return conn

def _init(conn: sqlite3.Connection):
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role in ('admin','student')),
        salt BLOB NOT NULL,
        pwhash BLOB NOT NULL
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS classes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        teacher TEXT,
        code TEXT,
        house TEXT,
        notes TEXT
    )""")
    conn.commit()

def seed_classes_if_empty():
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM classes")
    n = cur.fetchone()[0]
    if n == 0:
        cur.executemany("INSERT INTO classes(title,teacher,code,house,notes) VALUES(?,?,?,?,?)", [
            ("Maths Y12", "Ms. Lee", "R2", "Rutherford", "Bring calculator"),
            ("History Y11", "Mr. Patel", "M5", "Mansfield", "Essay due Friday"),
        ])
        conn.commit()
