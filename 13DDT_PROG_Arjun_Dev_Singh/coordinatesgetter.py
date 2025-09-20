"""
coordinatesgetter.py
---------------------
A Tkinter tool for selecting rectangular coordinates
on a static map image (e.g., buildings).
- Left click and drag to draw rectangle
- Coordinates are printed in console
"""

import tkinter as tk
from PIL import Image, ImageTk

# Path to map image (ensure file exists)
MAP_PATH = "images/map.jpg"

# Image display size
MAP_WIDTH = 1280
MAP_HEIGHT = 960


class CoordTool:
    """
    Coordinate selection tool.
    Lets user draw rectangles on a map to get (x, y) positions.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Building Coordinate Tool")

        # Load and resize image
        self.image = Image.open(MAP_PATH).resize((MAP_WIDTH, MAP_HEIGHT))
        self.tk_image = ImageTk.PhotoImage(self.image)

        # Canvas to hold image
        self.canvas = tk.Canvas(root, width=MAP_WIDTH, height=MAP_HEIGHT)
        self.canvas.pack()

        # Place image on canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_draw)       # Mouse down
        self.canvas.bind("<B1-Motion>", self.update_draw)     # Mouse move
        self.canvas.bind("<ButtonRelease-1>", self.finish_draw)  # Mouse up

        # Rectangle drawing vars
        self.rect = None
        self.start_x = 0
        self.start_y = 0

    def start_draw(self, event):
        """
        Start drawing rectangle on mouse press.
        """
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="red",
            width=2
        )

    def update_draw(self, event):
        """
        Update rectangle while dragging.
        """
        if self.rect:
            self.canvas.coords(
                self.rect,
                self.start_x,
                self.start_y,
                event.x,
                event.y
            )

    def finish_draw(self, event):
        """
        Finalize rectangle on mouse release.
        Print coordinates in console.
        """
        end_x, end_y = event.x, event.y

        # Ensure top-left and bottom-right order
        x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
        x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)

        print(f"Rectangle: Top-left=({x1}, {y1}), Bottom-right=({x2}, {y2})")
        print(f"BUILDINGS entry: (({x1}, {y1}), ({x2}, {y2})),\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = CoordTool(root)
    root.mainloop()
