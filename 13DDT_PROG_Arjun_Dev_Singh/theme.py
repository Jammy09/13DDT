
from tkinter import ttk
import tkinter as tk

PALETTE = {
    "bg": "#0B1220",
    "panel": "#111827",
    "accent": "#2563EB",
    "accent2": "#60A5FA",
    "text": "#E5E7EB",
    "muted": "#9CA3AF",
    "outline": "#1F2937",
    "code": "#38BDF8",
}

def init_style(root):
    style = ttk.Style(root)
    for base in ("clam","alt","default"):
        try: style.theme_use(base); break
        except tk.TclError: pass
    root.configure(bg=PALETTE["bg"])
    style.configure("App.TFrame", background=PALETTE["panel"])
    style.configure("App.TLabel", background=PALETTE["panel"], foreground=PALETTE["text"])
    style.configure("H1.TLabel", background=PALETTE["panel"], foreground=PALETTE["text"], font=("Segoe UI", 13, "bold"))
    style.configure("Ghost.TButton", background=PALETTE["panel"], foreground=PALETTE["text"], padding=6)
    style.configure("Status.TLabel", background=PALETTE["bg"], foreground=PALETTE["muted"], padding=6)
    style.configure("App.TCheckbutton", background=PALETTE["panel"], foreground=PALETTE["text"])
    return style, PALETTE