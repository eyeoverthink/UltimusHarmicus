# uqcb_artifacts.py
# Abstractions for algorithms, logic, color patterns, and charts stored in UQCB chain payloads.

from typing import Any, Dict, List, Optional, Tuple
import hashlib, json, base64

SCHEMA_VERSION = "1.0"


def sha256_hex_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))

# ---------------------
# Algorithm / Logic
# ---------------------

def encode_algorithm(name: str, description: str, pseudocode: List[str], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    body = {
        "type": "artifact/algorithm",
        "schema": SCHEMA_VERSION,
        "name": name,
        "description": description,
        "pseudocode": pseudocode,
        "params": params or {},
    }
    body["digest"] = sha256_hex_bytes(canonical_json(body).encode())
    return body


# ---------------------
# Color pattern (grid of RGB)
# ---------------------

def encode_color_pattern(name: str, grid: List[List[Tuple[int,int,int]]], palette_note: str = "") -> Dict[str, Any]:
    # Compact hex encoding per row: RRGGBB;...
    rows = []
    for row in grid:
        rows.append(''.join(f"{r:02x}{g:02x}{b:02x}" for (r,g,b) in row))
    body = {
        "type": "artifact/color_grid",
        "schema": SCHEMA_VERSION,
        "name": name,
        "rows_hex": rows,
        "width": len(grid[0]) if grid else 0,
        "height": len(grid),
        "note": palette_note,
    }
    body["digest"] = sha256_hex_bytes(canonical_json(body).encode())
    return body


def decode_color_pattern(rows_hex: List[str], width: int) -> List[List[Tuple[int,int,int]]]:
    grid: List[List[Tuple[int,int,int]]] = []
    for rh in rows_hex:
        row: List[Tuple[int,int,int]] = []
        for i in range(0, len(rh), 6):
            r = int(rh[i:i+2], 16)
            g = int(rh[i+2:i+4], 16)
            b = int(rh[i+4:i+6], 16)
            row.append((r,g,b))
        grid.append(row[:width])
    return grid

# ---------------------
# Chart (series) minimal representation
# ---------------------

def encode_chart(name: str, series: Dict[str, List[float]], note: str = "", image_png: Optional[bytes] = None) -> Dict[str, Any]:
    body: Dict[str, Any] = {
        "type": "artifact/chart",
        "schema": SCHEMA_VERSION,
        "name": name,
        "series": series,
        "note": note,
    }
    if image_png is not None:
        body["image_png_b64"] = base64.b64encode(image_png).decode()
    body["digest"] = sha256_hex_bytes(canonical_json(body).encode())
    return body


# ---------------------
# Reverse-engineering utilities (placeholders for user-defined logic)
# ---------------------

def infer_algorithm_from_colors(grid: List[List[Tuple[int,int,int]]]) -> Dict[str, Any]:
    # User-specific: map color patterns back to high-level hints.
    # Provide a simple heuristic example: dominant hue bands -> step segmentation.
    h, w = len(grid), len(grid[0]) if grid else 0
    return {"hypothesis": "color_bands_to_steps", "height": h, "width": w}


def series_from_color_grid(grid: List[List[Tuple[int,int,int]]]) -> Dict[str, List[float]]:
    # Example: convert brightness per column to a waveform
    if not grid:
        return {"brightness": []}
    h, w = len(grid), len(grid[0])
    col_vals: List[float] = []
    for x in range(w):
        s = 0.0
        for y in range(h):
            r,g,b = grid[y][x]
            s += 0.2126*r + 0.7152*g + 0.0722*b
        col_vals.append(s / h / 255.0)
    return {"brightness": col_vals}
