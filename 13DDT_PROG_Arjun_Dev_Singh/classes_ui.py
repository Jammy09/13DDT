import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db import get_db
from utils import CODE_PREFIX_TO_HOUSE, get_building_key

HOUSES = ["Batten","Hillary","Kupe","Mansfield","Rutherford","Snell","Te Kanawa","Upham"]

class ClassesWindow(tk.Toplevel):
    def __init__(self, parent, user, markers_norm, on_route_callback):
        super().__init__(parent)
        self.title("Classes")
        self.geometry("720x460"); self.resizable(True, True)
        self.user = user
        self.markers_norm = markers_norm
        self.on_route = on_route_callback

        cols = ("title","teacher","code","house","notes")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=14)
        self.tree.heading("title", text="Title");      self.tree.column("title", width=200, anchor="w")
        self.tree.heading("teacher", text="Teacher");  self.tree.column("teacher", width=140, anchor="w")
        self.tree.heading("code", text="Code");        self.tree.column("code", width=80, anchor="center")
        self.tree.heading("house", text="House");      self.tree.column("house", width=130, anchor="w")
        self.tree.heading("notes", text="Notes");      self.tree.column("notes", width=240, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        btns = ttk.Frame(self); btns.pack(fill="x", padx=10, pady=(0,10))
        ttk.Button(btns, text="Route to selected", command=self._route_selected).pack(side="left")
        # Remove the admin check so all users see the buttons:
        ttk.Button(btns, text="Add", command=self._add).pack(side="right", padx=4)
        ttk.Button(btns, text="Edit", command=self._edit).pack(side="right", padx=4)
        ttk.Button(btns, text="Delete", command=self._delete).pack(side="right", padx=4)

        self._refresh()

    def _refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        conn = get_db(); cur = conn.cursor()
        cur.execute("SELECT id,title,teacher,code,house,notes FROM classes ORDER BY title")
        for r in cur.fetchall():
            self.tree.insert("", "end", iid=str(r["id"]), values=(r["title"], r["teacher"] or "", r["code"] or "",
                                                                  r["house"] or "", r["notes"] or ""))

    def _route_selected(self):
        sel = self.tree.selection()
        if not sel: 
            messagebox.showwarning("Select a class", "Pick a class to route to."); 
            return
        iid = sel[0]
        conn = get_db(); cur = conn.cursor()
        cur.execute("SELECT * FROM classes WHERE id=?", (iid,))
        r = cur.fetchone()
        if not r: 
            messagebox.showerror("Error", "Could not load class row."); 
            return

        dest_house = (r["house"] or "").strip()
        if not dest_house and r["code"]:
            dest_house = CODE_PREFIX_TO_HOUSE.get(r["code"].strip().upper()[0], "")
        if not dest_house or dest_house not in self.markers_norm:
            messagebox.showerror("Missing house", "This class has no valid house set."); 
            return

        start = simpledialog.askstring("From where?", "Enter your starting house (e.g., Kupe):", parent=self)
        if not start: return
        start_key = get_building_key(start, self.markers_norm)
        if not start_key:
            messagebox.showerror("Invalid house", "Unknown starting house name."); 
            return

        self.on_route(start_key, dest_house)

    def _add(self):
        self._edit_dialog(None)

    def _edit(self):
        sel = self.tree.selection()
        if not sel: return
        iid = sel[0]
        conn = get_db(); cur = conn.cursor()
        cur.execute("SELECT * FROM classes WHERE id=?", (iid,))
        row = cur.fetchone()
        if row: self._edit_dialog(dict(row))

    def _edit_dialog(self, row=None):
        dlg = tk.Toplevel(self); dlg.title("Class"); dlg.grab_set()
        ttk.Label(dlg, text="Title").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        ttk.Label(dlg, text="Teacher").grid(row=1, column=0, sticky="w", padx=8, pady=6)
        ttk.Label(dlg, text="Room Code (e.g., R2)").grid(row=2, column=0, sticky="w", padx=8, pady=6)
        ttk.Label(dlg, text="House").grid(row=3, column=0, sticky="w", padx=8, pady=6)
        ttk.Label(dlg, text="Notes").grid(row=4, column=0, sticky="w", padx=8, pady=6)

        v_title = tk.StringVar(value=(row or {}).get("title",""))
        v_teacher = tk.StringVar(value=(row or {}).get("teacher",""))
        v_code = tk.StringVar(value=(row or {}).get("code",""))
        v_house = tk.StringVar(value=(row or {}).get("house",""))
        v_notes = tk.StringVar(value=(row or {}).get("notes",""))

        ttk.Entry(dlg, textvariable=v_title, width=36).grid(row=0, column=1, padx=8, pady=6)
        ttk.Entry(dlg, textvariable=v_teacher, width=36).grid(row=1, column=1, padx=8, pady=6)
        ttk.Entry(dlg, textvariable=v_code, width=18).grid(row=2, column=1, sticky="w", padx=8, pady=6)

        cb = ttk.Combobox(dlg, values=HOUSES, textvariable=v_house, width=16, state="readonly")
        cb.grid(row=3, column=1, sticky="w", padx=8, pady=6)

        ttk.Entry(dlg, textvariable=v_notes, width=36).grid(row=4, column=1, padx=8, pady=6)

        btns = ttk.Frame(dlg); btns.grid(row=5, column=1, sticky="e", padx=8, pady=10)

        def save():
            title = v_title.get().strip()
            teacher = v_teacher.get().strip() or None
            code = (v_code.get().strip().upper() or None)
            house = (v_house.get().strip() or None)
            if code and not house:
                house = CODE_PREFIX_TO_HOUSE.get(code[0])
            if not title:
                messagebox.showerror("Missing", "Title is required."); return
            conn = get_db(); cur = conn.cursor()
            if row and row.get("id"):
                cur.execute("UPDATE classes SET title=?,teacher=?,code=?,house=?,notes=? WHERE id=?",
                            (title, teacher, code, house, v_notes.get().strip() or None, row["id"]))
            else:
                cur.execute("INSERT INTO classes(title,teacher,code,house,notes) VALUES(?,?,?,?,?)",
                            (title, teacher, code, house, v_notes.get().strip() or None))
            conn.commit(); dlg.destroy(); self._refresh()

        ttk.Button(btns, text="Save", command=save).pack(side="right")
        ttk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="right", padx=8)

    def _delete(self):
        sel = self.tree.selection()
        if not sel: return
        if not messagebox.askyesno("Delete", "Delete selected class?"): return
        iid = sel[0]
        conn = get_db(); cur = conn.cursor()
        cur.execute("DELETE FROM classes WHERE id=?", (iid,)); conn.commit()
        self._refresh()