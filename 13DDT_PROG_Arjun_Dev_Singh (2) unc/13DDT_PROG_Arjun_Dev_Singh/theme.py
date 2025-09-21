"""
Theme and style configuration for the Macleans app.
Defines color palette and initializes ttk styles.
"""

import tkinter as tk
from tkinter import ttk

# ------------------ Color Palette ------------------
PALETTE = {
    "bg": "#0B1220",          # Background
    "panel": "#111827",       # Panel background
    "accent": "#2563EB",      # Primary accent
    "accent2": "#60A5FA",     # Secondary accent
    "text": "#E5E7EB",        # Main text
    "muted": "#9CA3AF",       # Muted text / status
    "outline": "#1F2937",     # Borders / outlines
    "code": "#38BDF8",        # Code highlight
}


def init_style(root: tk.Tk):
    """
    Initialize ttk styles for the application.

    Args:
        root (tk.Tk): Root tkinter window.

    Returns:
        tuple: (ttk.Style object, PALETTE dict)
    """
    style = ttk.Style(root)

    # Try to set a known theme
    for base in ("clam", "alt", "default"):
        try:
            style.theme_use(base)
            break
        except tk.TclError:
            continue

    # Configure root background
    root.configure(bg=PALETTE["bg"])

    # Frame styles
    style.configure("App.TFrame", background=PALETTE["panel"])

    # Label styles
    style.configure(
        "App.TLabel", background=PALETTE["panel"], foreground=PALETTE["text"]
    )
    style.configure(
        "H1.TLabel", background=PALETTE["panel"], foreground=PALETTE["text"],
        font=("Segoe UI", 13, "bold")
    )
    style.configure(
        "Status.TLabel", background=PALETTE["bg"], foreground=PALETTE["muted"], padding=6
    )

    # Button styles
    style.configure(
        "Ghost.TButton", background=PALETTE["panel"], foreground=PALETTE["text"], padding=6
    )

    # Checkbutton styles
    style.configure(
        "App.TCheckbutton", background=PALETTE["panel"], foreground=PALETTE["text"]
    )

    return style, PALETTE
