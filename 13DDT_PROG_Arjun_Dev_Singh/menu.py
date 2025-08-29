import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Default admin account
    cursor.execute("SELECT * FROM users")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "password"))
    conn.commit()
    conn.close()

# ---------------- LOGIN HANDLING ----------------
def attempt_login():
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        menu_root.destroy()
        import main   # goes to your main.py
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")

def register_user():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both fields!")
        return

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "User registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

# ---------------- GUI ----------------
def show_login_screen():
    global menu_root, username_entry, password_entry
    menu_root = tk.Tk()
    menu_root.title("Login - Macleans Navigator")
    menu_root.configure(bg="white")
    menu_root.iconbitmap("images/logo.ico")

    # FULLSCREEN
    menu_root.attributes("-fullscreen", True)
    menu_root.bind("<Escape>", lambda e: menu_root.attributes("-fullscreen", False))

    screen_width = menu_root.winfo_screenwidth()
    screen_height = menu_root.winfo_screenheight()

    # Background
    bg_image = Image.open("images/bg.png")
    bg_image = bg_image.resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(menu_root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo

    # Logo
    logo_img = Image.open("images/logo.ico")
    logo_img = logo_img.resize((120, 120))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(menu_root, image=logo_photo, bg="white")
    logo_label.image = logo_photo
    logo_label.pack(pady=(50, 20))

    # Title
    title_label = tk.Label(menu_root, text="Macleans Navigator", font=("Arial", 24, "bold"), bg="white")
    title_label.pack()

    # Username
    tk.Label(menu_root, text="Username:", font=("Arial", 14), bg="white").pack(pady=(40, 5))
    username_entry = tk.Entry(menu_root, font=("Arial", 14))
    username_entry.pack()

    # Password
    tk.Label(menu_root, text="Password:", font=("Arial", 14), bg="white").pack(pady=(20, 5))
    password_entry = tk.Entry(menu_root, font=("Arial", 14), show="*")
    password_entry.pack()

    # Buttons
    tk.Button(menu_root, text="Login", command=attempt_login,
              font=("Arial", 14), bg="#10E217", fg="white", padx=20, pady=8).pack(pady=20)

    tk.Button(menu_root, text="Register", command=register_user,
              font=("Arial", 14), bg="#0E6CFD", fg="white", padx=20, pady=8).pack()

    menu_root.mainloop()

# ---------------- RUN ----------------
if __name__ == "__main__":
    init_db()
    show_login_screen()
