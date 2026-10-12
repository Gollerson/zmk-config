#!/usr/bin/env python3
"""Render the dark/neon desktop wallpaper of the Eyelash Sofle keymap.

Usage:
    python3 scripts/render_wallpaper.py [output.png]

By default it writes keymap-wallpaper.png at the repository root.
Requires Pillow (PIL) and DejaVu fonts.
"""
import os
import re
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "keymap-wallpaper.png")

# ---------- palette ----------
BG_TOP = (6, 8, 14)
BG_BOT = (10, 14, 24)
PANEL = (13, 18, 29)
PANEL_EDGE = (28, 36, 54)
KEY = (25, 32, 46)
KEY_TOP = (34, 43, 61)
KEY_EDGE = (46, 58, 80)
TXT = (233, 239, 247)
TXT_DIM = (74, 86, 110)
TRANS = (12, 16, 25)
TRANS_EDGE = (24, 30, 44)

ACCENTS = {
    "base": (46, 230, 214),
    "sym": (179, 136, 255),
    "nav": (61, 220, 151),
    "sys": (255, 180, 84),
}

FKEY = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FKEY_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FTITLE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

def mix(c1, c2, t):
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c1, c2))

def dim(col, t):
    return mix(BG_TOP, col, t)

# ---------- layout data ----------
# each layer: (key, title, subtitle, [ (left[6], joy, right[n]) x5 ])
# '·' = transparent / no-op
L_BASE = [
    (["Esc", "1", "2", "3", "4", "5"], "↑", ["6", "7", "8", "9", "0", "?"]),
    (["Tab", "Q", "W", "E", "R", "T"], "↓", ["Y", "U", "I", "O", "P", "\\"]),
    (["Caps", "A", "S", "D", "F", "G"], "←", ["H", "J", "K", "L", ";", "'"]),
    (["Shft", "Z", "X", "C", "V", "B"], "→", ["N", "M", ",", ".", "/", "-"]),
    (["Mute", "Ctrl", "Gui", "Alt", "Space", "L1"], "Enter",
     ["Enter", "Bspc", "L2", "L3", "RShft"]),
]
L_SYM = [
    (["F1", "F2", "F3", "F4", "F5", "F6"], "↑", ["F7", "F8", "F9", "F10", "F11", "F12"]),
    (["!", "@", "#", "$", "%", "^"], "↓", ["&", "*", ":", "\"", "<", ">"]),
    (["`", "~", "=", "+", "_", "|"], "←", ["(", ")", "[", "]", "{", "}"]),
    (["-", "/", "\\", ";", "'", ","], "→", [".", "?", "·", "·", "·", "·"]),
    (["·", "·", "·", "·", "·", "·"], "·", ["·", "·", "·", "·", "·"]),
]
L_NAV = [
    (["ci\"", "ci'", "ci(", "ci[", "ci{", "va{"], "↑",
     ["*", "PgUp", "Home", "Up", "End", "PgDn"]),
    (["Esc", "·", "·", "·", "·", "·"], "↓", ["[m", "]m", "[[", "]]", "{", "}"]),
    (["Ctrl", "ciw", "\"+y", "\"+p", "\"_d", "·"], "←",
     ["#", "%", ":%s/", "=", ">>", "<<"]),
    (["Shft", "C-o", "C-i", "g;", "g,", "·"], "→",
     ["C-/", "C-F", "C-S", "C-B", "C-⇧P", "Del"]),
    (["·", "·", "·", "·", "·", "·"], "·", ["·", "·", "·", "·", "·"]),
]
L_SYS = [
    (["·", "BT\n1", "BT\n2", "BT\n3", "BT\n4", "BT\n5"], "↑",
     ["BT\nclr", "BT\nall", "Bri\n+", "Bri\n−", "Mute", "·"]),
    (["·", "USB", "BLE", "·", "·", "·"], "↓",
     ["Vol\n+", "Vol\n−", "Prev", "Play", "Next", "·"]),
    (["·", "Reset", "Boot", "·", "·", "·"], "←",
     ["Prt\nSc", "Lock", "·", "·", "·", "·"]),
    (["·", "Soft\noff", "RGB\noff", "RGB\non", "RGB\neff", "RGB\nbri"], "→",
     ["·", "·", "·", "·", "RGB\nbrd", "·"]),
    (["·", "·", "·", "·", "·", "·"], "·", ["·", "·", "·", "·", "·"]),
]

LAYERS = [
    ("base", "BASE", "QWERTY  ·  mods on thumbs  ·  encoder = volume", L_BASE),
    ("sym", "SYM", "every symbol  ·  ranked by BASE reach  ·  F-keys", L_SYM),
    ("nav", "NAV", "text objects  ·  motions  ·  search  ·  jump list", L_NAV),
    ("sys", "SYS", "bluetooth  ·  output  ·  media  ·  brightness  ·  rgb", L_SYS),
]

MODS = {"Esc", "Tab", "Caps", "Shft", "Ctrl", "Gui", "Alt", "Space",
        "Bspc", "Enter", "RShft", "Mute", "Del"}

# unshifted -> shifted legend (US QWERTY), printed small in the corner
SHIFT = {
    "1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&",
    "8": "*", "9": "(", "0": ")", "-": "_", ";": ":", "'": "\"",
    ",": "<", ".": ">", "/": "?", "\\": "|",
}

def role(label, key):
    if label in ("·", "", None):
        return "trans"
    if key == "sys":
        return "special"
    if label in MODS:
        return "mod"
    if re.fullmatch(r"L\d", label):
        return "layer"
    if re.fullmatch(r"F\d+", label):
        return "fn"
    return "char"

# ---------- geometry ----------
M, GAP = 34, 26
PW = (W - 2 * M - GAP) // 2
PH = (H - 2 * M - GAP) // 2

U = 76                      # key pitch (px)
KW = 68
KH = 66
RP = 76                     # row pitch
RAD = 11

COL_STAG = {0: 0.0, 1: 0.0, 2: -0.1875, 3: -0.3125, 4: -0.1875, 5: -0.125,
            7: 0.0,
            9: -0.125, 10: -0.1875, 11: -0.3125, 12: -0.1875, 13: 0.0, 14: 0.0}

# thumb vertical arc (units, outer -> inner)
THUMB_L = [0.06, 0.10, 0.18, 0.30, 0.46, 0.60]
THUMB_R = [0.60, 0.46, 0.30, 0.18, 0.10]   # inner -> outer


def rounded(d, box, r, **kw):
    try:
        d.rounded_rectangle(box, radius=r, **kw)
    except AttributeError:
        d.rectangle(box, **kw)


def fit_font(path, text, maxw, start):
    s = start
    while s > 9:
        f = font(path, s)
        w = max(f.getlength(line) for line in text.split("\n"))
        if w <= maxw:
            return f
        s -= 1
    return font(path, 9)


def draw_key(d, cx, cy, label, r, accent, icon=None, shift=None):
    x0, y0 = cx - KW // 2, cy - KH // 2
    box = (x0, y0, x0 + KW, y0 + KH)
    # shadow
    rounded(d, (x0 + 2, y0 + 4, x0 + KW + 2, y0 + KH + 4), RAD, fill=(3, 5, 9))
    if r == "trans":
        rounded(d, box, RAD, fill=TRANS, outline=TRANS_EDGE, width=1)
        d.text((cx, cy), "·", font=font(FKEY, 22), fill=(48, 58, 78), anchor="mm")
        return
    if r == "layer":
        fill = mix(dim(accent, 0.30), accent, 0.0)
        rounded(d, box, RAD, fill=dim(accent, 0.42), outline=accent, width=2)
        edge = accent
    elif r == "special":
        rounded(d, box, RAD, fill=mix(KEY, accent, 0.12), outline=dim(accent, 0.75), width=2)
        edge = dim(accent, 0.55)
    elif r == "mod":
        rounded(d, box, RAD, fill=KEY_TOP, outline=KEY_EDGE, width=1)
        edge = dim(accent, 0.55)
    elif r == "fn":
        rounded(d, box, RAD, fill=KEY, outline=KEY_EDGE, width=1)
        edge = dim(accent, 0.45)
    else:
        rounded(d, box, RAD, fill=KEY, outline=KEY_EDGE, width=1)
        edge = TXT
    # top sheen
    rounded(d, (x0 + 3, y0 + 3, x0 + KW - 3, y0 + 9), RAD - 3, fill=(255, 255, 255, 0))
    d.line((x0 + 5, y0 + 4, x0 + KW - 5, y0 + 4), fill=mix(fill if r == "layer" else KEY, (255, 255, 255), 0.10), width=1)
    if r == "layer":
        tcol = BG_TOP
    elif r == "special":
        tcol = accent
    elif r == "mod":
        tcol = mix(TXT, accent, 0.25)
    else:
        tcol = edge if r != "char" else TXT
    f = fit_font(FKEY_B if r in ("layer", "mod", "special") else FKEY,
                 label, KW - 12, 27)
    lines = label.split("\n")
    lh = f.size + 3
    total = lh * len(lines)
    y = cy - total / 2 + lh / 2 + (6 if shift else 0)
    for ln in lines:
        d.text((cx, y), ln, font=f, fill=tcol, anchor="mm")
        y += lh
    if shift:
        d.text((x0 + 9, y0 + 7), shift, font=font(FKEY, 18),
               fill=mix(TXT_DIM, TXT, 0.6), anchor="la")
    if icon == "knob":
        kx, ky, kr = x0 + KW - 15, y0 + 14, 8
        d.ellipse((kx - kr, ky - kr, kx + kr, ky + kr),
                  outline=dim(accent, 0.85), width=2)
        d.line((kx, ky - kr + 2, kx, ky - 1), fill=dim(accent, 0.9), width=2)
    elif icon == "home":
        d.ellipse((cx - 6, y0 + KH - 13, cx + 6, y0 + KH - 7), fill=dim(accent, 0.5))


def panel(d, ox, oy, key, title, subtitle, rows):
    accent = ACCENTS[key]
    # panel bg
    rounded(d, (ox, oy, ox + PW, oy + PH), 22, fill=PANEL, outline=PANEL_EDGE, width=2)
    # accent glow behind keyboard
    glow = Image.new("L", (PW, PH), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse((PW * 0.16, PH * 0.30, PW * 0.84, PH * 1.05), fill=26)
    gimg = Image.new("RGBA", (PW, PH), accent + (0,))
    gimg.putalpha(glow)
    d._image.paste(gimg, (ox, oy), gimg)
    # title
    d.text((ox + 44, oy + 34), title, font=font(FTITLE, 40), fill=accent)
    tw = font(FTITLE, 40).getlength(title)
    d.line((ox + 44, oy + 66, ox + 44 + tw, oy + 66), fill=dim(accent, 0.55), width=3)
    d.text((ox + 48 + tw + 20, oy + 44), subtitle, font=font(FKEY, 21), fill=TXT_DIM)
    # keyboard origin (top-left col0,row0 center)
    kb_w = 14 * U + KW
    ox0 = ox + (PW - kb_w) / 2 + KW / 2
    oy0 = oy + 108 + KH / 2

    def colx(u):
        return ox0 + u * U

    def rowy(r, u):
        return oy0 + r * RP + COL_STAG.get(u, 0) * U

    # joystick backing capsule
    jx = colx(7)
    jy0 = rowy(0, 7) - KH / 2 - 8
    jy1 = rowy(4, 7) + KH / 2 + 8
    rounded(d, (jx - KW / 2 - 8, jy0, jx + KW / 2 + 8, jy1), 16,
            fill=(10, 14, 22), outline=dim(accent, 0.40), width=1)
    d.text((jx, jy0 - 14), "5-WAY", font=font(FKEY_B, 13), fill=dim(accent, 0.45), anchor="mm")

    for r, (left, joy, right) in enumerate(rows):
        # left hand
        for i, lab in enumerate(left):
            ro = THUMB_L[i] if r == 4 else 0.0
            icon = None
            if key == "base" and lab == "Mute":
                icon = "knob"
            if key == "base" and lab in ("F", "J"):
                icon = "home"
            sh = SHIFT.get(lab) if key == "base" else None
            draw_key(d, colx(i), rowy(r, i) + ro * U, lab, role(lab, key),
                     accent, icon, sh)
        # joystick
        jr = "joy" if joy != "·" else "trans"
        draw_key(d, colx(7), rowy(r, 7) + (THUMB_L[5] if r == 4 else 0.0) * U,
                 joy, jr, accent)
        # right hand
        for i, lab in enumerate(right):
            u = 9 + i
            ro = THUMB_R[i] if r == 4 else 0.0
            sh = SHIFT.get(lab) if key == "base" else None
            draw_key(d, colx(u), rowy(r, u) + ro * U, lab, role(lab, key),
                     accent, None, sh)

    # (encoder press is drawn as the rotary icon on the Mute key)


def main():
    img = Image.new("RGB", (W, H), BG_TOP)
    d = ImageDraw.Draw(img)
    # background gradient
    for y in range(H):
        d.line((0, y, W, y), fill=mix(BG_TOP, BG_BOT, y / H))
    d._image = img
    # subtle dot grid
    for x in range(0, W, 40):
        for y in range(0, H, 40):
            d.point((x, y), fill=(20, 26, 40))

    for idx, (key, title, subtitle, rows) in enumerate(LAYERS):
        px = M + (idx % 2) * (PW + GAP)
        py = M + (idx // 2) * (PH + GAP)
        panel(d, px, py, key, title, subtitle, rows)

    # footer
    d.text((W / 2, H - 16), "PandaKB Eyelash Sofle  ·  nice!nano v2  ·  ZMK",
           font=font(FKEY, 18), fill=TXT_DIM, anchor="mm")
    img.save(OUT)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
