#!/usr/bin/env python3
"""Render one image summing up the world news of Monday 23 November 2026.

This is the source that drew entry.png. It is not the entrypoint: the
repository's main.py only copies the committed PNG to /output/entry.png,
which keeps the two sandbox runs byte-for-byte identical with no network
and no third-party packages at run time.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling factor for smooth edges
W = H = 1024 * S

BG = "#0d1626"
CARD = "#17243a"
CARD_ALT = "#14203a"
INK = "#f4f7fb"
MUTED = "#a9b7cb"
ACCENT = "#ff6b3d"
CYAN = "#57cdf0"
GREEN = "#7ee0a8"
LINE = "#2c3d59"

FONT_PATHS = {
    "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "reg": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
}
_fonts = {}


def font(kind, size):
    key = (kind, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_PATHS[kind], int(size * S))
    return _fonts[key]


def txt(d, xy, text, size, fill=INK, kind="bold", anchor=None):
    d.text((xy[0] * S, xy[1] * S), text, font=font(kind, size), fill=fill, anchor=anchor)


def rect(d, box, fill, outline=None, width=1, radius=0):
    b = tuple(v * S for v in box)
    if radius:
        d.rounded_rectangle(b, radius=radius * S, fill=fill, outline=outline, width=width * S)
    else:
        d.rectangle(b, fill=fill, outline=outline, width=width * S)


def line(d, pts, fill=LINE, width=2):
    d.line([(x * S, y * S) for x, y in pts], fill=fill, width=width * S, joint="curve")


def polygon(d, pts, fill):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill)


# --- icons: small, legible line art, drawn in a 72x72 box -------------------

def icon_globe(d, x, y, color=ACCENT):
    cx, cy, r = x + 36, y + 36, 27
    d.ellipse(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S),
              outline=color, width=3 * S)
    d.ellipse(((cx - 11) * S, (cy - r) * S, (cx + 11) * S, (cy + r) * S),
              outline=color, width=2 * S)
    line(d, [(cx - r, cy), (cx + r, cy)], fill=color, width=2)
    line(d, [(cx - r, cy - 12), (cx + r, cy - 12)], fill=color, width=1)
    line(d, [(cx - r, cy + 12), (cx + r, cy + 12)], fill=color, width=1)
    line(d, [(cx - 18, cy - 20), (cx - 4, cy - 6), (cx + 6, cy + 4),
             (cx + 20, cy + 19)], fill=INK, width=3)


def icon_building(d, x, y, color=ACCENT):
    rect(d, (x + 12, y + 18, x + 46, y + 56), CARD_ALT, outline=color, width=2)
    for row in (24, 36, 48):
        for col in (18, 30, 40):
            rect(d, (x + col, y + row, x + col + 5, y + row + 6), color, radius=1)
    polygon(d, [(x + 4, y + 58), (x + 20, y + 50), (x + 32, y + 59),
                (x + 48, y + 51), (x + 64, y + 60), (x + 64, y + 64),
                (x + 4, y + 64)], color)
    line(d, [(x + 50, y + 10), (x + 62, y + 10)], fill=CYAN, width=2)
    line(d, [(x + 56, y + 10), (x + 56, y + 16)], fill=CYAN, width=2)


def icon_capitol(d, x, y, color=CYAN):
    polygon(d, [(x + 10, y + 24), (x + 36, y + 10), (x + 62, y + 24)], color)
    rect(d, (x + 10, y + 24, x + 62, y + 28), color)
    for cx in (16, 27, 38, 49):
        rect(d, (x + cx, y + 29, x + cx + 7, y + 54), INK, radius=1)
    rect(d, (x + 8, y + 55, x + 64, y + 60), color)


def icon_chart(d, x, y, color=ACCENT):
    line(d, [(x + 8, y + 12), (x + 8, y + 60), (x + 64, y + 60)], fill=MUTED, width=2)
    pts = [(x + 12, y + 20), (x + 24, y + 30), (x + 34, y + 26),
           (x + 46, y + 44), (x + 60, y + 56)]
    line(d, pts, fill=color, width=4)
    polygon(d, [(x + 60, y + 56), (x + 48, y + 54), (x + 58, y + 44)], color)


def icon_flame(d, x, y, color=ACCENT):
    polygon(d, [(x + 36, y + 8), (x + 52, y + 30), (x + 57, y + 46),
                (x + 48, y + 60), (x + 24, y + 60), (x + 15, y + 46),
                (x + 24, y + 34), (x + 28, y + 42)], color)
    polygon(d, [(x + 36, y + 30), (x + 44, y + 46), (x + 28, y + 56),
                (x + 27, y + 44)], INK)


def icon_cap(d, x, y, color=CYAN):
    polygon(d, [(x + 6, y + 30), (x + 36, y + 14), (x + 66, y + 30),
                (x + 36, y + 46)], color)
    polygon(d, [(x + 20, y + 37), (x + 36, y + 44), (x + 52, y + 37),
                (x + 52, y + 56), (x + 36, y + 62), (x + 20, y + 56)], INK)
    line(d, [(x + 62, y + 32), (x + 62, y + 52)], fill=ACCENT, width=2)
    txt(d, (x + 27, y + 24), "AI", 12, BG, "bold")


def icon_ties(d, x, y, color=GREEN):
    d.ellipse(((x + 6) * S, (y + 24) * S, (x + 36) * S, (y + 54) * S),
              outline=color, width=3 * S)
    d.ellipse(((x + 36) * S, (y + 24) * S, (x + 66) * S, (y + 54) * S),
              outline=CYAN, width=3 * S)
    line(d, [(x + 28, y + 39), (x + 44, y + 39)], fill=INK, width=4)


def icon_warning(d, x, y, color=ACCENT):
    polygon(d, [(x + 36, y + 10), (x + 66, y + 60), (x + 6, y + 60)], color)
    rect(d, (x + 33, y + 27, x + 39, y + 47), BG)
    rect(d, (x + 33, y + 51, x + 39, y + 57), BG)


def icon_protest(d, x, y, color=CYAN):
    line(d, [(x + 20, y + 8), (x + 20, y + 64)], fill=MUTED, width=3)
    polygon(d, [(x + 22, y + 10), (x + 64, y + 18), (x + 60, y + 44),
                (x + 22, y + 40)], color)
    line(d, [(x + 32, y + 22), (x + 52, y + 26)], fill=BG, width=2)


ICONS = {
    "globe": icon_globe,
    "building": icon_building,
    "capitol": icon_capitol,
    "chart": icon_chart,
    "flame": icon_flame,
    "cap": icon_cap,
    "ties": icon_ties,
    "warning": icon_warning,
    "protest": icon_protest,
}


def card(d, x, y, w, h, tag, headline, sub, icon):
    rect(d, (x, y, x + w, y + h), CARD, outline=LINE, width=1, radius=10)
    rect(d, (x, y, x + 6, y + h), ACCENT, radius=3)
    ICONS[icon](d, x + 16, y + 10)
    tx = x + 96
    txt(d, (tx, y + 13), tag, 14, ACCENT, "bold")
    txt(d, (tx, y + 32), headline, 23, INK, "bold")
    txt(d, (tx, y + 63), sub, 14, MUTED, "reg")


def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # masthead
    txt(d, (44, 26), "THE WORLD · NEWS", 19, CYAN, "bold")
    txt(d, (44, 52), "MONDAY, 23 NOVEMBER 2026", 32, INK, "bold")
    rect(d, (44, 102, 980, 105), ACCENT)

    # lead story
    txt(d, (44, 118), "CLIMATE", 17, ACCENT, "bold")
    txt(d, (44, 140), "CLIMATE TALKS", 60, INK, "bold")
    txt(d, (44, 200), "COLLAPSE", 60, ACCENT, "bold")
    txt(d, (46, 276), "COP31 ends with no deal as oil states reject fossil-fuel", 18, MUTED, "reg")
    txt(d, (46, 298), "wording and climate finance stalls; longest UN talks ever", 18, MUTED, "reg")
    icon_globe(d, 838, 150)

    # story grid
    top = 344
    cw, ch, gx, gy = 456, 112, 16, 12
    rows = [
        [("UKRAINE", "Dymer strike: 11 dead", "Boy, 7, freed from rubble; Russian ship sunk", "building"),
         ("UNITED STATES", "Democrats win House", "Largest House majority since 1992", "capitol")],
        [("MARKETS", "AI sell-off hits", "Nasdaq erases all of its 2026 gains", "chart"),
         ("INDONESIA", "Factory fire: 24 dead", "Dozens missing after plant blaze", "flame")],
        [("SOUTH KOREA", "Minister resigns", "AI cheating scandal hits exams", "cap"),
         ("AFRICA", "Kenya–DRC ties restored", "WHO warns on Ebola-hit fighting", "ties")],
        [("MIDDLE EAST", "Gaza 'toxic wasteland'", "Study warns of long-term contamination", "warning"),
         ("FRANCE", "Protests grip cities", "Macron blames radical-left unrest", "protest")],
    ]
    for r, row in enumerate(rows):
        for c, (tag, head, sub, ic) in enumerate(row):
            card(d, 44 + c * (cw + gx), top + r * (ch + gy), cw, ch, tag, head, sub, ic)

    # closing strip
    rect(d, (44, 856, 980, 859), LINE)
    txt(d, (44, 872), "ALSO", 14, ACCENT, "bold")
    txt(d, (96, 872), "UK–EU deal in Commons  ·  Belgian airports shut by strike  ·  Myanmar genocide ruling", 14, MUTED, "reg")
    txt(d, (44, 902), "One image · 23 November 2026", 14, CYAN, "reg")

    out = img.resize((1024, 1024), Image.Resampling.LANCZOS)
    path = Path(__file__).resolve().parent / "entry.png"
    out.save(path, format="PNG", optimize=True)
    print(f"wrote {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
