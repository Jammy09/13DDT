
from typing import Tuple
from db import get_db
from utils import hash_password, verify_password, make_salt

ALLOWED_DOMAINS = {"macleans.school.nz", "macleans.nz"}

def _domain_ok(email: str) -> bool:
    if "@" not in email: return False
    return email.split("@",1)[1].lower() in ALLOWED_DOMAINS

def seed_admin_if_empty():
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users"); n = cur.fetchone()[0]
    if n == 0:
        salt = make_salt()
        pwhash = hash_password("admin123", salt)
        cur.execute("INSERT INTO users(email,name,role,salt,pwhash) VALUES(?,?,?,?,?)",
                    ("admin@macleans.school.nz","Admin","admin",salt,pwhash))
        conn.commit()

def register_user(email: str, name: str, password: str, role: str = "student") -> Tuple[bool, str]:
    email = email.strip().lower()
    if not _domain_ok(email):
        return False, "Email must be a Macleans address."
    if role not in ("admin","student"):
        role = "student"
    salt = make_salt()
    pwhash = hash_password(password, salt)
    try:
        conn = get_db(); cur = conn.cursor()
        cur.execute("INSERT INTO users(email,name,role,salt,pwhash) VALUES(?,?,?,?,?)",
                    (email, name.strip(), role, salt, pwhash))
        conn.commit()
        return True, "Registered."
    except Exception:
        return False, "That email is already registered."

def login_user(email: str, password: str):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email.strip().lower(),))
    row = cur.fetchone()
    if not row: return None, "No such user."
    if verify_password(password, row["salt"], row["pwhash"]):
        return {"id": row["id"], "email": row["email"], "name": row["name"], "role": row["role"]}, None
    return None, "Incorrect password."
