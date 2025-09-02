
from login import run_login_window
from map_viewer import MapApp
import tkinter as tk

if __name__ == "__main__":
    user = run_login_window()
    if not user:
        raise SystemExit(0)
    app = MapApp(user)
    tk.mainloop()
