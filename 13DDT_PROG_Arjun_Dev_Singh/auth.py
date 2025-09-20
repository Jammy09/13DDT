"""
auth.py
---------
Handles authentication logic:
- Checking allowed email domains
- Seeding an admin account if database is empty
- Registering new users
- Logging in users
"""

from typing import Tuple
from db import get_db
from utils import hash_password, verify_password, make_salt

# Allowed email domains for registration
ALLOWED_DOMAINS = {
    "macleans.school.nz",
    "macleans.nz",
    "student.macleans.school.nz",
}


def _domain_ok(email: str) -> bool:
    """
    Check if the email has an allowed domain.
    """
    if "@" not in email:
        return False

    # Extract domain after '@' and validate
    return email.split("@", 1)[1].lower() in ALLOWED_DOMAINS


def seed_admin_if_empty():
    """
    Create a default admin user if the database is empty.
    """
    conn = get_db()
    cur = conn.cursor()

    # Count users in DB
    cur.execute("SELECT COUNT(*) FROM users")
    n = cur.fetchone()[0]

    if n == 0:
        # Create admin with default password
        salt = make_salt()
        pwhash = hash_password("admin123", salt)

        cur.execute(
            """
            INSERT INTO users(email, name, role, salt, pwhash)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("admin@macleans.school.nz", "Admin", "admin", salt, pwhash),
        )
        conn.commit()


def register_user(email: str, name: str, password: str) -> Tuple[bool, str]:
    """
    Register a new user.
    Returns (success, message).
    """
    if not _domain_ok(email):
        return False, "Registration failed: Invalid email domain."

    conn = get_db()
    cur = conn.cursor()

    # Ensure no duplicate account
    cur.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cur.fetchone():
        return False, "Registration failed: User already exists."

    # Salt + password hash
    salt = make_salt()
    pwhash = hash_password(password, salt)

    # Insert into DB
    cur.execute(
        """
        INSERT INTO users(email, name, role, salt, pwhash)
        VALUES (?, ?, ?, ?, ?)
        """,
        (email, name, "user", salt, pwhash),
    )
    conn.commit()

    return True, "Registration successful!"


def login_user(email: str, password: str) -> Tuple[bool, str, str]:
    """
    Attempt login.
    Returns (success, message, name).
    """
    conn = get_db()
    cur = conn.cursor()

    # Fetch user data
    cur.execute("SELECT name, salt, pwhash FROM users WHERE email = ?", (email,))
    row = cur.fetchone()

    if not row:
        return False, "Login failed: User not found.", ""

    name, salt, pwhash = row

    # Check password
    if verify_password(password, salt, pwhash):
        return True, "Login successful!", name

    return False, "Login failed: Incorrect password.", ""
