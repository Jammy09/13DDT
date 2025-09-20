"""
classes_ui.py
---------------
Holds reusable Tkinter UI classes.
"""

import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    """
    A frame with vertical scrolling capability.
    Useful for content larger than the window.
    """

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # Create canvas for scrolling content
        canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        # Frame inside canvas to hold widgets
        self.scrollable_frame = ttk.Frame(canvas)

        # Attach inner frame to canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Scroll wheel binding
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Configure canvas scrolling
        canvas.configure(yscrollcommand=scrollbar.set)

        # Layout
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
