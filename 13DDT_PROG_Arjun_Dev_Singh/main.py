
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import heapq

# Map settings
MAP_PATH = "images/map.jpg"
MAP_WIDTH, MAP_HEIGHT = 1000, 698

# Building coordinates (approx from map)
BUILDINGS = {
    "Batten": (890, 600),
    "Kupe": (870, 170),
    "Rutherford": (800, 330),
    "Te Kanawa": (520, 160),
    "Upham": (150, 490),
    "Mansfield": (940, 400),
    "Snell": (330, 420),
    "Hillary": (570, 340),
}

GRID_SCALE = 3  # lower = more precise, slower
SAT_MAX = 40    # road detection sensitivity
VAL_MIN = 200

class Pathfinder:
    def __init__(self, img):
        self.img = img.convert("HSV").resize((MAP_WIDTH//GRID_SCALE, MAP_HEIGHT//GRID_SCALE))
        self.pixels = self.img.load()
        self.w, self.h = self.img.size

    def is_walkable(self, x, y):
        if not (0 <= x < self.w and 0 <= y < self.h):
            return False
        h, s, v = self.pixels[x, y]
        return s < SAT_MAX and v > VAL_MIN

    def heuristic(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def neighbors(self, node):
        x, y = node
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x+dx, y+dy
            if self.is_walkable(nx, ny):
                yield (nx, ny)

    def astar(self, start, goal):
        start = (start[0]//GRID_SCALE, start[1]//GRID_SCALE)
        goal = (goal[0]//GRID_SCALE, goal[1]//GRID_SCALE)

        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                break

            for nxt in self.neighbors(current):
                new_cost = cost_so_far[current] + 1
                if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                    cost_so_far[nxt] = new_cost
                    priority = new_cost + self.heuristic(goal, nxt)
                    heapq.heappush(frontier, (priority, nxt))
                    came_from[nxt] = current

        # reconstruct path
        if goal not in came_from:
            return []

        path = []
        node = goal
        while node:
            path.append((node[0]*GRID_SCALE, node[1]*GRID_SCALE))
            node = came_from[node]
        return path[::-1]

class MapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Navigator")
        self.root.geometry(f"{MAP_WIDTH+200}x{MAP_HEIGHT+50}")

        self.original_image = Image.open(MAP_PATH).resize((MAP_WIDTH, MAP_HEIGHT))
        self.display_image = self.original_image.copy()
        self.tk_image = ImageTk.PhotoImage(self.display_image)

        self.canvas = tk.Canvas(root, width=MAP_WIDTH, height=MAP_HEIGHT)
        self.canvas.grid(row=0, column=0, rowspan=6)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        self.pathfinder = Pathfinder(self.original_image)

        # Dropdowns
        self.start_var = tk.StringVar()
        self.end_var = tk.StringVar()

        ttk.Label(root, text="Start:").grid(row=0, column=1, sticky="w")
        self.start_menu = ttk.Combobox(root, textvariable=self.start_var, values=list(BUILDINGS.keys()))
        self.start_menu.grid(row=1, column=1)

        ttk.Label(root, text="Destination:").grid(row=2, column=1, sticky="w")
        self.end_menu = ttk.Combobox(root, textvariable=self.end_var, values=list(BUILDINGS.keys()))
        self.end_menu.grid(row=3, column=1)

        self.route_btn = ttk.Button(root, text="Show Route", command=self.draw_route)
        self.route_btn.grid(row=4, column=1, pady=10)

        self.clear_btn = ttk.Button(root, text="Clear", command=self.clear_route)
        self.clear_btn.grid(row=5, column=1)

    def draw_route(self):
        start = self.start_var.get()
        end = self.end_var.get()
        if start not in BUILDINGS or end not in BUILDINGS:
            print("Invalid selection.")
            return

        start_xy = BUILDINGS[start]
        end_xy = BUILDINGS[end]
        path = self.pathfinder.astar(start_xy, end_xy)

        img = self.original_image.copy()
        draw = ImageDraw.Draw(img)

        if path:
            draw.line(path, fill="red", width=3)

        r = 6
        draw.ellipse([start_xy[0]-r, start_xy[1]-r, start_xy[0]+r, start_xy[1]+r], fill="green")
        draw.ellipse([end_xy[0]-r, end_xy[1]-r, end_xy[0]+r, end_xy[1]+r], fill="blue")

        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.itemconfig(self.image_on_canvas, image=self.tk_image)

    def clear_route(self):
        self.tk_image = ImageTk.PhotoImage(self.original_image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = MapApp(root)
    root.mainloop()

