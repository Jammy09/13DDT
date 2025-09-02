
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from theme import init_style, PALETTE
from utils import (
    find_map_image, MAP_PATH, load_markers_norm, raster_route_walkways,
    get_building_key
)

SCALES = [0.75, 1.0, 1.25, 1.5, 1.75, 2.0]

class MapApp:
    def __init__(self, user):
        self.root = tk.Tk()
        self.root.title(f"Macleans — Campus Map  —  {user['name']} ({user['role']})")
        sw = self.root.winfo_screenwidth(); sh = self.root.winfo_screenheight()
        w = max(860, min(int(sw*0.7), 1200)); h = max(600, min(int(sh*0.7), 800))
        self.root.geometry(f"{w}x{h}"); self.root.minsize(860, 600)
        self.style, self.palette = init_style(self.root)
        self.user = user

        self.scale_index = 1; self.offset_x = 0; self.offset_y = 0
        self.markers_norm = load_markers_norm()
        self._path_points_norm = []; self.highlight=None

        try:
            map_path = find_map_image() or MAP_PATH
            self.base_image = Image.open("C:/Users/arjun/Downloads/Macleans_Map_App_v6_0_3_classes_fix/images/map.jpg")
        except Exception:
            messagebox.showerror("Map not found","Put a .jpg/.jpeg/.png in the 'images' folder (macleans_map.jpg).")
            self.root.destroy(); return

        self._ui(); self._bind(); self._redraw_all()

    def _to_px(self, xn, yn):
        return (xn*self.base_image.width, yn*self.base_image.height)

    def _ui(self):
        top = ttk.Frame(self.root, style="App.TFrame", padding=(10,8)); top.pack(side="top", fill="x")
        ttk.Label(top, text="Macleans Campus Map", style="H1.TLabel").pack(side="left", padx=(0,10))

        ttk.Label(top, text="From:", style="App.TLabel").pack(side="left", padx=(12,0))
        names = sorted(self.markers_norm.keys()); self.from_var = tk.StringVar(); self.to_var = tk.StringVar()
        ttk.Combobox(top, textvariable=self.from_var, values=names, width=14).pack(side="left", padx=2)
        ttk.Label(top, text="To:", style="App.TLabel").pack(side="left")
        ttk.Combobox(top, textvariable=self.to_var, values=names, width=14).pack(side="left", padx=2)
        ttk.Button(top, text="Route", style="Ghost.TButton", command=self._do_route).pack(side="left", padx=8)
        ttk.Button(top, text="Classes", style="Ghost.TButton", command=self._open_classes).pack(side="left", padx=6)

        tools = ttk.Frame(top, style="App.TFrame"); tools.pack(side="right")
        ttk.Button(tools, text=" + ", style="Ghost.TButton", command=lambda: self._zoom_step(+1, None)).pack(side="left", padx=2)
        ttk.Button(tools, text=" - ", style="Ghost.TButton", command=lambda: self._zoom_step(-1, None)).pack(side="left", padx=2)
        ttk.Button(tools, text="Reset View", style="Ghost.TButton", command=self._reset_view).pack(side="left", padx=6)
        ttk.Button(tools, text="Logout", style="Ghost.TButton", command=self._logout).pack(side="left", padx=6)

        self.canvas = tk.Canvas(self.root, bg=self.palette["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.img_item=None
        self.status = tk.StringVar(value="Walkways-only routing; starts/ends at your exact house pins.")
        ttk.Label(self.root, textvariable=self.status, style="Status.TLabel").pack(side="bottom", fill="x")

    def _bind(self):
        self.canvas.bind("<ButtonPress-3>", self._on_pan_press)
        self.canvas.bind("<B3-Motion>", self._on_pan_drag)
        self.canvas.bind("<ButtonRelease-3>", self._on_pan_release)
        self.root.bind("<MouseWheel>", self._zoom_wheel)
        self.root.bind("<Control-MouseWheel>", self._zoom_wheel)
        self.root.bind("<Button-4>", lambda e: self._zoom_step(+1, (e.x, e.y)))
        self.root.bind("<Button-5>", lambda e: self._zoom_step(-1, (e.x, e.y)))
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _redraw_all(self):
        scale = SCALES[self.scale_index]
        w = int(self.base_image.width * scale); h = int(self.base_image.height * scale)
        self.current_img = ImageTk.PhotoImage(self.base_image.resize((w,h)), master=self.root)
        if self.img_item is None:
            self.img_item = self.canvas.create_image(self.offset_x, self.offset_y, anchor="nw", image=self.current_img)
        else:
            self.canvas.itemconfigure(self.img_item, image=self.current_img)
            self.canvas.coords(self.img_item, self.offset_x, self.offset_y)
        self._redraw_overlays()

    def _redraw_overlays(self):
        for item in self.canvas.find_all():
            if item != self.img_item: self.canvas.delete(item)
        scale = SCALES[self.scale_index]

        if self._path_points_norm:
            pts=[]
            for xn,yn in self._path_points_norm:
                x,y = self._to_px(xn,yn)
                pts.extend([x*scale + self.offset_x, y*scale + self.offset_y])
            self.canvas.create_line(*pts, width=4, fill="#EF4444", capstyle="round", joinstyle="round")

        for name,(xn,yn) in self.markers_norm.items():
            x,y = self._to_px(xn,yn)
            cx,cy = x*scale + self.offset_x, y*scale + self.offset_y
            r=7
            self.canvas.create_oval(cx-r*2, cy-r*2, cx+r*2, cy+r*2, outline="#1D4ED8", width=2)
            self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="#FBBF24", outline="#0B1220", width=1)
            self.canvas.create_text(cx+10, cy-12, text=name, anchor="w", fill="#E5E7EB", font=("Segoe UI", 10))

    def _on_pan_press(self, ev): self._pan_start=(ev.x,ev.y); self._panning=False
    def _on_pan_drag(self, ev):
        sx,sy = getattr(self,"_pan_start",(ev.x,ev.y)); dx,dy = ev.x-sx, ev.y-sy
        if not getattr(self,"_panning",False):
            if abs(dx)+abs(dy) < 6: return
            self._panning=True
        self.offset_x += dx; self.offset_y += dy; self._pan_start=(ev.x,ev.y); self._redraw_all()
    def _on_pan_release(self, ev): self._panning=False

    def _zoom_wheel(self, ev):
        step = +1 if getattr(ev,"delta",0) > 0 else -1
        self._zoom_step(step, (ev.x, ev.y))

    def _zoom_step(self, step, anchor):
        new_index = max(0, min(self.scale_index + step, len(SCALES)-1))
        if new_index == self.scale_index: return
        old = SCALES[self.scale_index]; new = SCALES[new_index]
        if anchor is None:
            cw = self.canvas.winfo_width() or 1000; ch = self.canvas.winfo_height() or 700
            anchor = (cw//2, ch//2)
        ax,ay = anchor
        img_x = (ax - self.offset_x)/old; img_y = (ay - self.offset_y)/old
        self.scale_index = new_index
        self.offset_x = int(ax - img_x*new); self.offset_y = int(ay - img_y*new)
        self._redraw_all()

    def _reset_view(self):
        self.scale_index = 1; self.offset_x = 0; self.offset_y = 0
        self._path_points_norm=[]; self._redraw_all()

    def _do_route(self):
        a = get_building_key(self.from_var.get(), self.markers_norm)
        b = get_building_key(self.to_var.get(), self.markers_norm)
        if not a or not b:
            messagebox.showerror("Error", "Choose valid From and To."); return
        pts = raster_route_walkways(a, b, self.markers_norm, self.base_image)
        if not pts:
            messagebox.showwarning("No path", "No walkway route found between those buildings."); return
        self._path_points_norm = pts
        if True:  # no auto-center toggle in this build
            self._center_on_name(b)

    def _center_on_name(self, name: str):
        x,y = self._to_px(*self.markers_norm.get(name, (None,None)))
        if x is None: return
        if self.scale_index < 2: self.scale_index = 2
        sc = SCALES[self.scale_index]
        cw = self.canvas.winfo_width() or 1000; ch = self.canvas.winfo_height() or 700
        self.offset_x = int(cw//2 - x*sc); self.offset_y = int(ch//2 - y*sc); self._redraw_all()

    def _open_classes(self):
        from classes_ui import ClassesWindow
        def route_from_to(a_house, b_house):
            self.from_var.set(a_house); self.to_var.set(b_house); self._do_route()
        ClassesWindow(self.root, self.user, self.markers_norm, route_from_to)

    def _logout(self):
        from login import clear_session
        clear_session()
        messagebox.showinfo("Logged out", "Session cleared. Please relaunch the app to sign in again.")
        self.root.destroy()

    def _on_close(self): self.root.destroy()
