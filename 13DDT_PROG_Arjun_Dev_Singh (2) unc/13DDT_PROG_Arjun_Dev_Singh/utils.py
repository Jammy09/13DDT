"""
Utility functions for Macleans Campus App.

Includes:
- File paths
- Marker and building handling
- Walkway routing
- Password hashing and verification
"""

from pathlib import Path
import json
import re
import os
import hashlib
import hmac
from collections import deque
import heapq
from PIL import Image

# ------------------ Paths ------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
IMG_DIR = BASE_DIR / "images"
MAP_PATH = IMG_DIR / "macleans_map.jpg"
MARKERS_PATH = DATA_DIR / "markers.json"
CODES_PATH = DATA_DIR / "codes.json"

# ------------------ Default Markers ------------------
DEFAULT_MARKERS_NORM = {
    "Te Kanawa": [0.4339, 0.4215],
    "Kupe": [0.7615, 0.4172],
    "Rutherford": [0.8116, 0.5930],
    "Mansfield": [0.8597, 0.6933],
    "Batten": [0.8096, 0.8299],
    "Hillary": [0.5571, 0.5044],
    "Snell": [0.3437, 0.6105],
    "Upham": [0.2054, 0.6177],
}

ALIASES = {
    "tk": "Te Kanawa",
    "te kanawa": "Te Kanawa",
    "tekanawa": "Te Kanawa",
}

CODE_PREFIX_TO_HOUSE = {
    "K": "Kupe",
    "M": "Mansfield",
    "R": "Rutherford",
    "T": "Te Kanawa",
    "U": "Upham",
    "S": "Snell",
    "H": "Hillary",
    "B": "Batten",
}

CODE_RE = re.compile(r"^[A-Za-z]{1,2}\d{1,3}$")

# ------------------ Directory Helpers ------------------
def ensure_dirs():
    """Ensure DATA_DIR and IMG_DIR exist."""
    DATA_DIR.mkdir(exist_ok=True)
    IMG_DIR.mkdir(exist_ok=True)

# ------------------ Marker Load/Save ------------------
def load_markers_norm():
    """Load normalized markers from JSON, fallback to defaults."""
    ensure_dirs()
    if MARKERS_PATH.exists():
        try:
            data = json.loads(MARKERS_PATH.read_text(encoding="utf-8"))
            if data.get("_format") == "norm":
                return {k: tuple(v) for k, v in data["points"].items()}
        except Exception:
            pass
    return {k: tuple(v) for k, v in DEFAULT_MARKERS_NORM.items()}


def save_markers_norm(points: dict):
    """Save normalized markers to JSON."""
    ensure_dirs()
    MARKERS_PATH.write_text(
        json.dumps({"_format": "norm", "points": points}, indent=2),
        encoding="utf-8",
    )


# ------------------ Code Load/Save ------------------
def load_codes_norm():
    """Load room codes from JSON, fallback to empty dict."""
    ensure_dirs()
    if CODES_PATH.exists():
        try:
            return {k.upper(): tuple(v) for k, v in json.loads(CODES_PATH.read_text(encoding="utf-8")).items()}
        except Exception:
            pass
    return {}


def save_codes_norm(codes: dict):
    """Save room codes to JSON."""
    ensure_dirs()
    CODES_PATH.write_text(json.dumps(codes, indent=2), encoding="utf-8")


# ------------------ House / Code Helpers ------------------
def is_code(token: str) -> bool:
    """Check if string is a valid room code."""
    return bool(token and CODE_RE.match(token.strip()))


def get_house_for_code(code: str):
    """Get the house for a given room code based on prefix."""
    code = code.strip().upper()
    for p, h in CODE_PREFIX_TO_HOUSE.items():
        if code.startswith(p):
            return h
    return None


def get_building_key(name: str, markers: dict):
    """Return canonical building/house name from input string."""
    if not name:
        return None
    n = " ".join(name.strip().split()).lower()
    m = {k.lower(): k for k in markers}
    if n in m:
        return m[n]
    if n in ALIASES:
        return ALIASES[n]
    return None


def find_map_image():
    """Find a map image in IMG_DIR, preferring largest if multiple."""
    for name in ["macleans_map.jpg", "macleans_map.jpeg", "macleans_map.png"]:
        p = IMG_DIR / name
        if p.exists():
            return p
    cand = []
    for p in IMG_DIR.glob("*.*"):
        if p.suffix.lower() in {".jpg", ".jpeg", ".png"}:
            cand.append((p.stat().st_size, p))
    if cand:
        cand.sort(reverse=True)
        return cand[0][1]
    return None


# ------------------ Walkway Routing ------------------
def raster_route_walkways(
    start_house: str,
    end_house: str,
    markers_norm: dict,
    pil_image,
    grid_scale: int = 3,
    sat_max: int = 40,
    val_min: int = 200,
):
    """
    Walkways-only route using HSV threshold + A* on a grid.
    Starts and ends at exact house pins.
    """
    w0, h0 = pil_image.width, pil_image.height
    ax0, ay0 = markers_norm[start_house]
    bx0, by0 = markers_norm[end_house]

    # Start and end in pixel coordinates
    sx, sy = int(ax0 * w0), int(ay0 * h0)
    tx, ty = int(bx0 * w0), int(by0 * h0)

    hsv = pil_image.convert("HSV").resize(
        (max(1, w0 // grid_scale), max(1, h0 // grid_scale))
    )
    pix = hsv.load()
    W, H = hsv.size

    def walkable(x, y):
        if not (0 <= x < W and 0 <= y < H):
            return False
        h, s, v = pix[x, y]
        return s < sat_max and v > val_min

    # Snap start and end to nearest walkable
    def nearest_walk(c):
        if walkable(*c):
            return c
        q = deque([c])
        seen = {c}
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if (nx, ny) in seen:
                    continue
                if 0 <= nx < W and 0 <= ny < H:
                    if walkable(nx, ny):
                        return (nx, ny)
                    seen.add((nx, ny))
                    q.append((nx, ny))
        return c

    s = nearest_walk((sx // grid_scale, sy // grid_scale))
    t = nearest_walk((tx // grid_scale, ty // grid_scale))

    # A* pathfinding
    def h(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    frontier = [(0, s)]
    came = {s: None}
    g = {s: 0}

    while frontier:
        _, u = heapq.heappop(frontier)
        if u == t:
            break
        x, y = u
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            v = (x + dx, y + dy)
            if not walkable(*v):
                continue
            nv = g[u] + 1
            if v not in g or nv < g[v]:
                g[v] = nv
                came[v] = u
                heapq.heappush(frontier, (nv + h(v, t), v))

    # Reconstruct path
    if t not in came and t != s:
        return []

    path = []
    cur = t
    while cur is not None:
        px, py = cur[0] * grid_scale, cur[1] * grid_scale
        path.append((px / w0, py / h0))
        cur = came.get(cur)
    path.reverse()

    if path:
        path[0] = (ax0, ay0)
        path[-1] = (bx0, by0)
    else:
        path = [(ax0, ay0), (bx0, by0)]
    return path


# ------------------ Password Hashing ------------------
def make_salt(n: int = 16) -> bytes:
    """Generate cryptographically secure random salt."""
    return os.urandom(n)


def hash_password(password: str, salt: bytes, rounds: int = 200_000) -> bytes:
    """Hash password using PBKDF2-HMAC-SHA256."""
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, rounds)


def verify_password(password: str, salt: bytes, pwhash: bytes, rounds: int = 200_000) -> bool:
    """Verify password against stored hash using constant-time comparison."""
    test = hash_password(password, salt, rounds)
    return hmac.compare_digest(test, pwhash)
