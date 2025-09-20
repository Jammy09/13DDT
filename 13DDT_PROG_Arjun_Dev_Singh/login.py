"""
Login and registration GUI for Macleans app.
Includes session management and password validation.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import json
import re

from auth import seed_admin_if_empty, register_user, login_user
from db import seed_classes_if_empty

# Base directory and session file path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SESSION_PATH = DATA_DIR / "session.json"


# ------------------ User Class ------------------
class User:
    """Represents a logged-in user."""

    def __init__(self, user_data):
        if isinstance(user_data, list):
            self.id, self.email, self.name, self.role = user_data[:4]
        elif isinstance(user_data, dict):
            self.id = user_data.get("id")
            self.email = user_data.get("email")
            self.name = user_data.get("name")
            self.role = user_data.get("role")
        else:
            raise ValueError("Invalid user data type")

    def to_dict(self):
        """Return user data as a dictionary."""
        return {"id": self.id, "email": self.email, "name": self.name, "role": self.role}


# ------------------ Session Manager ------------------
class SessionManager:
    """Handles saving, loading, and clearing session data."""

    @staticmethod
    def save(user: User):
        """Save the current user session to a JSON file."""
        DATA_DIR.mkdir(exist_ok=True)
        SESSION_PATH.write_text(json.dumps(user.to_dict()), encoding="utf-8")

    @staticmethod
    def load():
        """Load session from file if it exists."""
        try:
            data = json.loads(SESSION_PATH.read_text(encoding="utf-8"))
            return User(data)
        except Exception:
            return None

    @staticmethod
    def clear():
        """Clear saved session."""
        try:
            SESSION_PATH.unlink()
        except Exception:
            pass


# ------------------ Password Validator ------------------
class PasswordValidator:
    """Validates password strength."""

    @staticmethod
    def validate(password: str):
        """Check password against required rules."""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter."
        if not re.search(r"[0-9]", password):
            return False, "Password must contain at least one number."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character."
        return True, ""


# ------------------ Login Window ------------------
class LoginWindow:
    """GUI window for login and registration."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Macleans — Sign in")
        self.root.geometry("440x340")
        self.root.resizable(False, False)

        # Seed initial admin and classes if DB empty
        seed_admin_if_empty()
        seed_classes_if_empty()

        # Notebook for Sign in / Register tabs
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill="both", expand=True, padx=12, pady=12)

        self.user = None
        self._create_signin_tab()
        self._create_register_tab()

        # Load existing session
        sess = SessionManager.load()
        if sess:
            self.user = sess
            self.root.after(200, self.root.quit)

    # ------------------ Tabs ------------------
    def _create_signin_tab(self):
        """Create Sign in tab."""
        f1 = ttk.Frame(self.nb, padding=14)
        self.nb.add(f1, text="Sign in")

        ttk.Label(f1, text="Email").grid(row=0, column=0, sticky="w")
        ttk.Label(f1, text="Password").grid(row=1, column=0, sticky="w")

        self.si_email = tk.StringVar()
        self.si_pass = tk.StringVar()
        ttk.Entry(f1, textvariable=self.si_email, width=36).grid(row=0, column=1, pady=6)
        ttk.Entry(f1, textvariable=self.si_pass, show="•", width=36).grid(row=1, column=1, pady=6)

        ttk.Button(f1, text="Sign in", command=self._do_login).grid(row=2, column=1, sticky="e", pady=10)

    def _create_register_tab(self):
        """Create Register tab."""
        f2 = ttk.Frame(self.nb, padding=14)
        self.nb.add(f2, text="Register")

        self.r_email = tk.StringVar()
        self.r_name = tk.StringVar()
        self.r_pass = tk.StringVar()

        ttk.Label(f2, text="Email (@macleans...)").grid(row=0, column=0, sticky="w")
        ttk.Entry(f2, textvariable=self.r_email, width=36).grid(row=0, column=1, pady=6)
        ttk.Label(f2, text="Name").grid(row=1, column=0, sticky="w")
        ttk.Entry(f2, textvariable=self.r_name, width=36).grid(row=1, column=1, pady=6)
        ttk.Label(f2, text="Password").grid(row=2, column=0, sticky="w")
        ttk.Entry(f2, textvariable=self.r_pass, show="•", width=36).grid(row=2, column=1, pady=6)
        ttk.Button(f2, text="Register", command=self._do_register).grid(row=3, column=1, sticky="e", pady=10)

    # ------------------ Actions ------------------
    def _do_login(self):
        """Handle user login."""
        email = self.si_email.get().strip()
        pwd = self.si_pass.get()
        u, err = login_user(email, pwd)
        if err:
            messagebox.showerror("Login failed", err)
            return

        self.user = User(u)
        SessionManager.save(self.user)
        self.root.quit()

    def _do_register(self):
        """Handle new user registration."""
        email = self.r_email.get().strip()
        name = self.r_name.get().strip()
        password = self.r_pass.get().strip()

        valid, msg = PasswordValidator.validate(password)
        if not valid:
            messagebox.showerror("Register failed", msg)
            return

        ok, err_msg = register_user(email, name, password, role="student")
        if err_msg:
            messagebox.showerror("Register failed", err_msg)
            return

        messagebox.showinfo("Registered", "Registered successfully. You can sign in now.")
        self.nb.select(0)  # Switch to Sign in tab


# ------------------ Run ------------------
def run_login_window():
    """Run the login window and return the logged-in user."""
    lw = LoginWindow()
    lw.root.mainloop()
    try:
        lw.root.destroy()
    except Exception:
        pass
    return lw.user
