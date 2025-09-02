
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import json
from auth import seed_admin_if_empty, register_user, login_user
from db import seed_classes_if_empty

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SESSION_PATH = DATA_DIR / "session.json"

def save_session(user: dict):
    DATA_DIR.mkdir(exist_ok=True)
    SESSION_PATH.write_text(json.dumps(user), encoding="utf-8")

def load_session():
    try:
        return json.loads(SESSION_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None

def clear_session():
    try: SESSION_PATH.unlink()
    except Exception: pass

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Macleans — Sign in")
        self.root.geometry("440x340"); self.root.resizable(False, False)

        seed_admin_if_empty(); seed_classes_if_empty()

        self.nb = ttk.Notebook(self.root); self.nb.pack(fill="both", expand=True, padx=12, pady=12)

        # Sign in tab
        f1 = ttk.Frame(self.nb, padding=14); self.nb.add(f1, text="Sign in")
        ttk.Label(f1, text="Email").grid(row=0, column=0, sticky="w")
        ttk.Label(f1, text="Password").grid(row=1, column=0, sticky="w")
        self.si_email = tk.StringVar(); self.si_pass = tk.StringVar()
        ttk.Entry(f1, textvariable=self.si_email, width=36).grid(row=0, column=1, pady=6)
        ttk.Entry(f1, textvariable=self.si_pass, show="•", width=36).grid(row=1, column=1, pady=6)
        ttk.Button(f1, text="Sign in", command=self._do_login).grid(row=2, column=1, sticky="e", pady=10)

        # Register tab
        f2 = ttk.Frame(self.nb, padding=14); self.nb.add(f2, text="Register")
        self.r_email = tk.StringVar(); self.r_name = tk.StringVar(); self.r_pass = tk.StringVar()
        ttk.Label(f2, text="Email (@macleans...)").grid(row=0, column=0, sticky="w")
        ttk.Entry(f2, textvariable=self.r_email, width=36).grid(row=0, column=1, pady=6)
        ttk.Label(f2, text="Name").grid(row=1, column=0, sticky="w")
        ttk.Entry(f2, textvariable=self.r_name, width=36).grid(row=1, column=1, pady=6)
        ttk.Label(f2, text="Password").grid(row=2, column=0, sticky="w")
        ttk.Entry(f2, textvariable=self.r_pass, show="•", width=36).grid(row=2, column=1, pady=6)
        ttk.Button(f2, text="Register", command=self._do_register).grid(row=3, column=1, sticky="e", pady=10)

        sess = load_session()
        if sess:
            self.user = sess
            self.root.after(200, self.root.quit)
        else:
            self.user = None

    def _do_login(self):
        email = self.si_email.get().strip()
        pwd = self.si_pass.get()
        u, err = login_user(email, pwd)
        if err:
            messagebox.showerror("Login failed", err); return
        save_session(u); self.user = u; self.root.quit()

    def _do_register(self):
        ok, msg = register_user(self.r_email.get(), self.r_name.get(), self.r_pass.get(), role="student")
        if ok:
            messagebox.showinfo("Registered", "Registered successfully. You can sign in now."); 
            self.nb.select(0)
        else:
            messagebox.showerror("Register failed", msg)

def run_login_window():
    lw = LoginWindow()
    lw.root.mainloop()
    try: lw.root.destroy()
    except Exception: pass
    return lw.user
