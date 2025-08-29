import tkinter as tk
from PIL import Image, ImageTk

MAP_PATH = "images/map.jpg"  # make sure this path is correct

MAP_WIDTH = 1280
MAP_HEIGHT = 960

class CoordTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Building Coordinate Tool")

        self.image = Image.open(MAP_PATH).resize((MAP_WIDTH, MAP_HEIGHT))
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.canvas = tk.Canvas(root, width=MAP_WIDTH, height=MAP_HEIGHT)
        self.canvas.pack()

        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        # Events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.update_draw)
        self.canvas.bind("<ButtonRelease-1>", self.finish_draw)

        self.rect = None
        self.start_x = self.start_y = 0

    def start_draw(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def update_draw(self, event):
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def finish_draw(self, event):
        end_x, end_y = event.x, event.y
        x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
        x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)
        print(f"Rectangle: Top-left=({x1}, {y1}), Bottom-right=({x2}, {y2})")
        print(f"BUILDINGS entry: ( ({x1}, {y1}), ({x2}, {y2}) ),\n")

root = tk.Tk()
app = CoordTool(root)
root.mainloop()
