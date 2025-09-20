"""
User authentication and registration module.

Handles:
- Domain validation
- Admin seeding (if DB empty)
- User registration
- User login
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
    Check if the email belongs to an allowed domain.

    Args:
        email (str): Email address to validate.

    Returns:
        bool: True if the domain is allowed, False otherwise.
    """
    if "@" not in email:
        return False
    domain = email.split("@", 1)[1].lower()
    return domain in ALLOWED_DOMAINS


def seed_admin_if_empty() -> None:
    """
    Create a default admin user if the users table is empty.
    """
    conn = get_db()
    cur = conn.cursor()

    # Count existing users
    cur.execute("SELECT COUNT(*) FROM users")
    user_count = cur.fetchone()[0]

    if user_count == 0:
        # Create admin credentials
        salt = make_salt()
        pwhash = hash_password("admin123", salt)

        # Insert default admin into the database
        cur.execute(
            """
            INSERT INTO users (email, name, role, salt, pwhash)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("admin@macleans.school.nz", "Admin", "admin", salt, pwhash),
        )
        conn.commit()


def register_user(
    email: str,
    name: str,
    password: str,
    role: str = "student",
) -> Tuple[bool, str]:
    """
    Register a new user in the database.

    Args:
        email (str): User's email address.
        name (str): User's display name.
        password (str): Plaintext password to hash.
        role (str): Role of the user ("admin" or "student").

    Returns:
        Tuple[bool, str]: (success flag, message).
    """
    email = email.strip().lower()

    # Validate email domain
    if not _domain_ok(email):
        return False, "Email must be a Macleans address."

    # Restrict role to valid options
    if role not in ("admin", "student"):
        role = "student"

    # Generate salt and hashed password
    salt = make_salt()
    pwhash = hash_password(password, salt)

    try:
        conn = get_db()
        cur = conn.cursor()

        # Attempt to insert user into DB
        cur.execute(
            """
            INSERT INTO users (email, name, role, salt, pwhash)
            VALUES (?, ?, ?, ?, ?)
            """,
            (email, name.strip(), role, salt, pwhash),
        )
        conn.commit()
        return True, "Registered."
    except Exception:
        # Likely a unique constraint failure (duplicate email)
        return False, "That email is already registered."


def login_user(email: str, password: str):
    """
    Authenticate a user by email and password.

    Args:
        email (str): User's email.
        password (str): Plaintext password to verify.

    Returns:
        Tuple[dict | None, str | None]:
            - If successful: (user dict, None)
            - If failure: (None, error message)
    """
    conn = get_db()
    cur = conn.cursor()

    # Fetch user record
    cur.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),))
    row = cur.fetchone()

    if not row:
        return None, "No such user."

    # Verify password using stored salt + hash
    if verify_password(password, row["salt"], row["pwhash"]):
        return {
            "id": row["id"],
            "email": row["email"],
            "name": row["name"],
            "role": row["role"],
        }, None

    return None, "Incorrect password."
