
"""
Main entry point for the Macleans app.
Handles login and launches the main map application.
"""

import tkinter as tk
from login import run_login_window
from map_viewer import MapApp


if __name__ == "__main__":
    # Run login window and get the authenticated user
    user = run_login_window()
    
    # Exit if login was cancelled or failed
    if not user:
        raise SystemExit(0)
    
    # Launch the main MapApp with the logged-in user
    app = MapApp(user)
    tk.mainloop()
