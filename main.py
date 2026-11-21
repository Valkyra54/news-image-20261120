#!/usr/bin/env python3
"""THE FRIDAY GAZETTE — one broadsheet image summing up Friday 20 November 2026.

Draws 1024x1024 entry.png with PIL only. Deterministic: no randomness, no
timestamps, no network. Output dir honours MAKEFUN_OUTPUT_DIR (default /output).
37 verified stories (RESEARCH-V2.md, cutoff ~12:10 UTC Fri 20 Nov 2026; refreshed Sat 21 Nov 2026 per REFRESH-RESULT.md).
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

# ---- palette (warm broadsheet paper, ink, red, navy) ----
PAPER = (247, 243, 234)
PAPER_DARK = (238, 231, 216)
INK = (28, 28, 28)
INK_SOFT = (74, 74, 74)
MUTED = (120, 116, 104)
RED = (163, 22, 33)
RED_DARK = (128, 16, 26)
RED_PALE = (250, 226, 226)
NAVY = (27, 42, 74)
NAVY_DARK = (16, 26, 50)
SKY = (207, 224, 234)
TEAL = (38, 110, 118)
SAND = (214, 196, 158)
GOLD = (198, 148, 52)
RULE = (180, 172, 152)
OCEAN = (213, 228, 236)
LAND = (226, 216, 188)
LAND2 = (205, 214, 178)

SERIF_B = os.path.join(BASE, "fonts", "DejaVuSerif-Bold.ttf")
SANS = os.path.join(BASE, "fonts", "DejaVuSans.ttf")
SANS_B = os.path.join(BASE, "fonts", "DejaVuSans-Bold.ttf")


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap by pixel width. Deterministic."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, fill, max_w, lh, max_lines=None):
    """Draw wrapped text, return y just below last line."""
    lines = wrap(d, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def chip(d, x, y, text, font, fg=(255, 255, 255), bg=RED, pad_x=7, h=18):
    w = int(d.textlength(text, font=font)) + pad_x * 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=bg)
    d.text((x + pad_x, y + 3), text, font=font, fill=fg)
    return x + w


def rule(d, x0, x1, y, fill=RULE, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- masthead
def draw_masthead(d):
    rule(d, 16, 1008, 8, fill=INK, width=3)
    title = "THE FRIDAY GAZETTE"
    tf = F(SERIF_B, 47)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 14), title, font=tf, fill=INK)
    sub = F(SANS_B, 21)
    date = "FRIDAY 20 NOVEMBER 2026"
    dw = d.textlength(date, font=sub)
    d.text(((W - dw) / 2, 66), date, font=sub, fill=RED)
    small = F(SANS_B, 12)
    d.text((16, 71), "FRIDAY EDITION", font=small, fill=INK_SOFT)
    right = "37 STORIES  •  5 CONTINENTS"
    d.text((1008 - d.textlength(right, font=small), 71), right, font=small, fill=INK_SOFT)
    rule(d, 16, 1008, 94, fill=INK, width=2)
    rule(d, 16, 1008, 97, fill=INK, width=1)


# ---------------------------------------------------------------- lead art
def draw_kyiv(d, x, y, w, h):
    """Night sky over Kyiv: missiles, bridges, river, explosions."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY_DARK)
    # fixed stars (no randomness)
    for sx, sy, r in [(18, 12, 1), (52, 26, 1), (96, 10, 2), (140, 30, 1),
                      (180, 14, 1), (220, 28, 2), (262, 12, 1), (300, 22, 1),
                      (34, 44, 1), (120, 48, 1), (200, 44, 1), (285, 48, 1)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=(235, 235, 220))
    # crescent moon
    d.ellipse([x + 268, y + 8, x + 292, y + 32], fill=(240, 228, 170))
    d.ellipse([x + 276, y + 5, x + 298, y + 29], fill=NAVY_DARK)
    # missile streaks (bright heads + trails)
    for (x0, y0, x1, y1) in [(40, 6, 96, 44), (150, 2, 196, 40), (230, 10, 262, 34)]:
        d.line([(x + x0, y + y0), (x + x1, y + y1)], fill=(255, 210, 120), width=2)
        d.ellipse([x + x1 - 3, y + y1 - 3, x + x1 + 3, y + y1 + 3], fill=(255, 220, 140))
    # explosion glows
    for cx, cy, r in [(70, 62, 9), (210, 58, 7)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=(255, 140, 40))
        d.ellipse([x + cx - r // 2, y + cy - r // 2, x + cx + r // 2, y + cy + r // 2],
                  fill=(255, 220, 120))
    # skyline silhouettes
    for bx, bw, bh in [(0, 26, 26), (30, 18, 34), (52, 30, 22), (86, 20, 30),
                       (110, 34, 20), (148, 22, 32), (174, 28, 24), (206, 20, 30),
                       (230, 30, 22), (264, 26, 28), (294, 26, 20)]:
        d.rectangle([x + bx, y + h - 30 - bh, x + bx + bw, y + h - 14], fill=(10, 16, 32))
    # river + three bridges
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(43, 74, 122))
    for bx in (28, 128, 228):
        d.arc([x + bx, y + h - 30, x + bx + 56, y + h - 2], 180, 360, fill=(240, 228, 170), width=3)
        d.line([(x + bx + 28, y + h - 30), (x + bx + 28, y + h - 14)], fill=(240, 228, 170), width=2)


def draw_akvan(d, x, y, w, h):
    """Cyclone spiral over the Odisha coast."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    cx, cy = x + 150, y + 48
    # spiral: concentric arcs, rotating start angles
    for i, r in enumerate(range(12, 46, 8)):
        start = 20 + i * 55
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 250, fill=TEAL, width=5)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 255, 255))
    # land (Odisha coast) bottom right
    d.polygon([(x + 170, y + h), (x + 320, y + h), (x + 320, y + 62),
               (x + 268, y + 70), (x + 210, y + 82)], fill=SAND)
    d.line([(x + 170, y + h), (x + 210, y + 82), (x + 268, y + 70), (x + 320, y + 62)],
           fill=(120, 100, 60), width=2)
    # rain streaks
    for rx, ry in [(16, 14), (34, 34), (52, 12), (70, 40), (88, 18), (104, 44)]:
        d.line([(x + rx, y + ry), (x + rx - 5, y + ry + 12)], fill=(90, 130, 160), width=2)
    # shelter roofs on the coast
    for hx in (230, 258, 286):
        d.polygon([(x + hx, y + 78), (x + hx + 12, y + 70), (x + hx + 24, y + 78)], fill=RED)


def draw_cop(d, x, y, w, h):
    """COP31 hall: rows of desks + the slashed draft, 144 -> 80."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 220, 200))
    # back wall panel
    d.rectangle([x + 14, y + 8, x + w - 14, y + 30], fill=(198, 178, 140))
    d.text((x + 22, y + 12), "ANTALYA  •  COP31", font=F(SANS_B, 11), fill=(90, 70, 40))
    # rows of desks with delegates
    for row, ry in enumerate((40, 58, 76)):
        for col in range(6):
            dx = x + 16 + col * 50
            d.rectangle([dx, y + ry, dx + 40, y + ry + 10], fill=(138, 122, 90))
            d.ellipse([dx + 15, y + ry - 9, dx + 25, y + ry + 1], fill=(60, 55, 45))
    # the draft document, centre foreground
    d.rectangle([x + 96, y + 30, x + 224, y + h - 6], fill=(255, 255, 255), outline=(150, 140, 120))
    d.text((x + 108, y + 36), "DRAFT", font=F(SANS_B, 11), fill=MUTED)
    barf = F(SANS_B, 22)
    d.text((x + 108, y + 52), "144 → 80", font=barf, fill=RED)
    d.line([(x + 106, y + 50), (x + 214, y + 78)], fill=RED, width=3)
    # mini bar chart: 144 vs 80 paragraphs
    d.rectangle([x + 240, y + 44, x + 258, y + h - 12], fill=(170, 160, 140))
    d.rectangle([x + 264, y + 62, x + 282, y + h - 12], fill=RED)

LEADS = [
    {
        "art": "kyiv",
        "tag": "WAR • UKRAINE",
        "headline": "RUSSIA'S BIGGEST STRIKE HITS UKRAINE",
        "chips": ["110+ MISSILES", "~400 DRONES", "9 DEAD"],
        "deck": "Three Kyiv bridges hit, power cut in five districts; Poland scrambles NATO jets.",
        "source": "CNN • THE TIMES • REUTERS • BBC",
    },
    {
        "art": "akvan",
        "tag": "DISASTER • INDIA",
        "headline": "CYCLONE AKVAN SLAMS ODISHA",
        "chips": ["~370,000 EVACUATED", "70–80 KM/H", "209 MM RAIN"],
        "deck": "Landfall near Gopalpur; 423 rescue teams out, 69 trains cancelled, no deaths.",
        "source": "IMD • REUTERS",
    },
    {
        "art": "cop",
        "tag": "CLIMATE • ANTALYA",
        "headline": "COP31: NO DEAL ON FINAL DAY",
        "chips": ["0 FOSSIL MENTIONS", "$120BN CUT", "144 → 80"],
        "deck": "Draft slashed to 80 paragraphs; talks spill into the weekend. Türkiye inks $26bn+.",
        "source": "REUTERS • UN NEWS • AP",
    },
]

ART = {"kyiv": draw_kyiv, "akvan": draw_akvan, "cop": draw_cop}


def draw_lead(d, x, y, lead):
    w = 320
    ART[lead["art"]](d, x, y, w, 84)
    ty = y + 88
    d.text((x, ty), lead["tag"], font=F(SANS_B, 10), fill=RED)
    sf = F(SANS_B, 8)
    d.text((x + w - d.textlength(lead["source"], font=sf), ty + 1),
           lead["source"], font=sf, fill=MUTED)
    text_block(d, x, y + 102, lead["headline"], F(SERIF_B, 18), INK, w, 19, max_lines=2)
    cy = y + 144
    cx = x
    for c in lead["chips"]:
        cx = chip(d, cx, cy, c, F(SANS_B, 10), h=16) + 6
    text_block(d, x, y + 164, lead["deck"], F(SANS, 11), INK_SOFT, w, 12, max_lines=2)


def draw_leads(d):
    for i, lead in enumerate(LEADS):
        draw_lead(d, 16 + i * 336, 104, lead)


# ---------------------------------------------------------------- tiles
# 11 stories 4-14 + Bitcoin market-chart tile (story 16) = 12 cells.
TILES = [
    {"num": 4, "tag": "MARKETS • TOKYO", "kind": "chart-nikkei",
     "headline": "AI SELL-OFF SLAMS ASIAN MARKETS",
     "deck": "Nikkei −5.06%; US: S&P −3.7%, Nasdaq −5.3%.",
     "source": "REUTERS • WSJ"},
    {"num": 5, "tag": "EUROPE • BRUSSELS",
     "headline": "BREXIT RESET AGREED — FEES HOLD IT UP",
     "deck": "Deal agreed Friday; the EU won't implement it until fees are settled.",
     "source": "BBC • THE TIMES"},
    {"num": 6, "tag": "IRAQ • MIDDLE EAST",
     "headline": "IRAQI TROOPS ENTER HEZBOLLAH STRONGHOLD",
     "deck": "Forces move into Jurf al-Sakhar under a deal; 9 officials sacked.",
     "source": "REUTERS • CNA"},
    {"num": 7, "tag": "TECH • CHINA",
     "headline": "US CHIP RULES HIT CHINA'S AI STOCKS",
     "deck": "New curbs on advanced AI chips; TSMC limits Chinese designers to 28nm.",
     "source": "REUTERS"},
    {"num": 8, "tag": "LAW • NEW YORK", "stamp": "STILL OUT",
     "headline": "HUAWEI JURY STILL OUT — NO VERDICT",
     "deck": "Deliberating since Wednesday. Still no verdict.",
     "source": "REUTERS"},
    {"num": 9, "tag": "US POLITICS • WASHINGTON",
     "headline": "TRUMP: 'VERY GOOD TALKS' WITH PUTIN",
     "deck": "90 minutes on his Asia trip; 'very good talks' with Putin on Ukraine.",
     "source": "FOX NEWS • REUTERS"},
    {"num": 10, "tag": "ENERGY • GLOBAL", "kind": "chart-oil",
     "headline": "OIL SLIDES FOR A THIRD WEEK",
     "deck": "Brent $92.57, WTI $83.98 (Fri close).",
     "source": "REUTERS"},
    {"num": 11, "tag": "POLAND • NATO",
     "headline": "POLAND SCRAMBLES NATO JETS",
     "deck": "Tusk: 'deliberate provocation'; two missiles fell, Patriots on alert.",
     "source": "REUTERS • CNN"},
    {"num": 12, "tag": "CYBER • BRITAIN",
     "headline": "SECRET OP SAVES FRIDGES FROM HACKERS",
     "deck": "Flaw in RDM cooling controllers; devices pulled offline, food kept cold.",
     "source": "BBC • REUTERS"},
    {"num": 13, "tag": "SECURITY • SYDNEY",
     "headline": "SYDNEY CAR-BOMB PLOT: 3 ARRESTED",
     "deck": "Raids across west Sydney; one man charged over alleged IED documents.",
     "source": "AP • REUTERS"},
    {"num": 14, "tag": "HEALTH • BARCELONA",
     "headline": "PANCREATIC PILL: TUMOURS VANISH IN 1 OF 12",
     "deck": "Daraxonrasib + chemo: 60.7% response in an early trial; “closest to cure”.",
     "source": "BBC"},
    {"num": 16, "tag": "CRYPTO • GLOBAL", "kind": "chart-btc",
     "headline": "BITCOIN BELOW $60,000",
     "deck": "BTC ~$58,300, lowest since Sep 2024.",
     "source": "FINNHUB • COINDESK"},
]


def draw_mini_bars(d, x, y, w, h, items):
    """Negative bars hanging from a zero line. items: (label, pct)."""
    zero = y + 2
    d.line([(x, zero), (x + w, zero)], fill=INK_SOFT, width=1)
    bw = (w - (len(items) - 1) * 14) // len(items)
    lab_f = F(SANS_B, 9)
    for i, (lab, pct) in enumerate(items):
        bx = x + i * (bw + 14)
        bh = max(3, int(16 * min(abs(pct), 7.0) / 7.0))
        d.rectangle([bx, zero + 2, bx + bw, zero + 2 + bh], fill=RED)
        d.text((bx, zero + 5 + bh), lab, font=lab_f, fill=INK)
        d.text((bx, zero + 15 + bh), f"{pct:+.1f}%", font=F(SANS_B, 8), fill=RED)


def draw_btc_line(d, x, y, w, h):
    """Falling line crossing below a dashed $60,000 line."""
    # dashed reference line at $60,000
    ry = y + 14
    for dx in range(0, w, 10):
        d.line([(x + dx, ry), (x + dx + 6, ry)], fill=RED, width=2)
    d.text((x + w - 52, ry - 12), "$60,000", font=F(SANS_B, 9), fill=RED)
    pts = [(0, 4), (0.2, 8), (0.4, 12), (0.55, 20), (0.7, 26), (0.85, 32), (1.0, 38)]
    xy = [(x + int(px * w), y + py) for px, py in pts]
    d.line(xy, fill=NAVY, width=3, joint="curve")
    d.ellipse([xy[-1][0] - 4, xy[-1][1] - 4, xy[-1][0] + 4, xy[-1][1] + 4], fill=RED)
    d.text((x, y + h - 11), "$58,317", font=F(SANS_B, 10), fill=RED)


def draw_tile(d, x, y, tile):
    w, h = 242, 102
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=RULE)
    d.text((x + 8, y + 5), tile["tag"], font=F(SANS_B, 9), fill=RED)
    num = str(tile["num"])
    nf = F(SANS_B, 10)
    nw = d.textlength(num, font=nf)
    d.ellipse([x + w - 12 - nw, y + 4, x + w - 4, y + 18], fill=NAVY)
    d.text((x + w - 8 - nw, y + 5), num, font=nf, fill=(255, 255, 255))
    kind = tile.get("kind")
    if kind == "chart-nikkei":
        text_block(d, x + 8, y + 20, tile["headline"], F(SERIF_B, 13), INK, w - 16, 15, max_lines=1)
        draw_mini_bars(d, x + 8, y + 36, w - 16, 38,
                       [("NIKKEI", -5.1), ("KOSPI", -5.2), ("TAIEX", -6.2)])
        d.text((x + 8, y + 78), tile["deck"], font=F(SANS, 9), fill=INK_SOFT)
        d.text((x + 8, y + 90), tile["source"], font=F(SANS_B, 8), fill=MUTED)
    elif kind == "chart-oil":
        text_block(d, x + 8, y + 20, tile["headline"], F(SERIF_B, 13), INK, w - 16, 15, max_lines=1)
        draw_mini_bars(d, x + 8, y + 36, w - 16, 38,
                       [("BRENT −3.4%/WK", -3.4), ("WTI −5.2%/WK", -5.2)])
        d.text((x + 8, y + 78), tile["deck"], font=F(SANS, 9), fill=INK_SOFT)
        d.text((x + 8, y + 90), tile["source"], font=F(SANS_B, 8), fill=MUTED)
    elif kind == "chart-btc":
        text_block(d, x + 8, y + 20, tile["headline"], F(SERIF_B, 13), INK, w - 16, 15, max_lines=1)
        draw_btc_line(d, x + 8, y + 36, w - 16, 38)
        d.text((x + 8, y + 78), tile["deck"], font=F(SANS, 9), fill=INK_SOFT)
        d.text((x + 8, y + 90), tile["source"], font=F(SANS_B, 8), fill=MUTED)
    else:
        text_block(d, x + 8, y + 20, tile["headline"], F(SERIF_B, 14), INK, w - 16, 16, max_lines=2)
        text_block(d, x + 8, y + 58, tile["deck"], F(SANS, 10), INK_SOFT, w - 16, 12, max_lines=2)
        if tile.get("stamp"):
            sf = F(SANS_B, 9)
            sw = d.textlength(tile["stamp"], font=sf) + 12
            d.rounded_rectangle([x + w - sw - 6, y + 82, x + w - 6, y + 96], radius=3,
                                outline=RED, width=2)
            d.text((x + w - sw, y + 85), tile["stamp"], font=sf, fill=RED)
        d.text((x + 8, y + 88), tile["source"], font=F(SANS_B, 8), fill=MUTED)


def draw_tiles(d):
    lab = F(SANS_B, 13)
    d.text((16, 300), "THE DAY IN BRIEF", font=lab, fill=INK)
    d.text((1008 - d.textlength("STORIES 4–14  •  CHARTS IN RED", font=F(SANS_B, 10)), 302),
           "STORIES 4–14  •  CHARTS IN RED", font=F(SANS_B, 10), fill=MUTED)
    rule(d, 16, 1008, 318, fill=INK, width=1)
    for i, tile in enumerate(TILES):
        col, row = i % 4, i // 4
        draw_tile(d, 16 + col * 250, 324 + row * 110, tile)

# ---------------------------------------------------------------- map band
# Simplified flat world map, drawn in band-local coordinates (0..992 x 0..112).
CONTINENTS = [
    # North America
    [(8, 18), (60, 8), (110, 6), (150, 10), (170, 22), (150, 30), (130, 26),
     (120, 40), (100, 55), (80, 70), (60, 78), (45, 60), (30, 45), (15, 30)],
    # Greenland
    [(185, 4), (205, 2), (215, 10), (200, 16), (188, 12)],
    # South America
    [(120, 72), (150, 68), (175, 78), (180, 95), (160, 112), (140, 100), (125, 85)],
    # Europe
    [(430, 20), (470, 12), (500, 18), (495, 30), (470, 28), (455, 38), (440, 30)],
    # Africa
    [(430, 45), (480, 42), (510, 50), (505, 75), (480, 95), (460, 90), (445, 65), (428, 55)],
    # Asia
    [(500, 15), (600, 8), (700, 10), (800, 14), (860, 25), (840, 45), (780, 55),
     (720, 60), (680, 75), (640, 55), (600, 45), (560, 40), (520, 30)],
    # Australia
    [(800, 85), (850, 80), (880, 88), (860, 100), (820, 100), (795, 92)],
    # UK + Japan dots
    [(425, 16), (432, 14), (434, 22), (428, 24)],
    [(872, 26), (878, 24), (880, 32), (874, 34)],
    # New Zealand
    [(922, 96), (930, 94), (932, 104), (924, 106)],
]
CONTINENT_FILLS = [LAND, LAND, LAND2, LAND, LAND2, LAND, LAND2, LAND, LAND, LAND]

# (number, x, y) — hand-placed on the drawn shapes (§F of RESEARCH-V2)
PINS = [
    (1, 500, 22),    # Kyiv
    (2, 700, 58),    # Odisha
    (3, 486, 40),    # Antalya
    (4, 876, 30),    # Tokyo
    (5, 458, 18),    # Brussels
    (6, 520, 44),    # Jurf al-Sakhar
    (7, 140, 32),    # New York
    (8, 138, 42),    # Washington
    (9, 424, 16),    # London
    (10, 440, 32),   # Paris
    (11, 868, 94),   # Sydney
    (12, 927, 100),  # Wellington
]


def draw_map(d):
    lab = F(SANS_B, 13)
    d.text((16, 654), "WHERE IT HAPPENED", font=lab, fill=INK)
    d.text((1008 - d.textlength("12 PLACES  •  FRIDAY 20 NOVEMBER 2026", font=F(SANS_B, 10)), 656),
           "12 PLACES  •  FRIDAY 20 NOVEMBER 2026", font=F(SANS_B, 10), fill=MUTED)
    rule(d, 16, 1008, 672, fill=INK, width=1)
    mx, my, mw, mh = 16, 676, 992, 112
    d.rectangle([mx, my, mx + mw, my + mh], fill=OCEAN, outline=RULE)
    for poly, fill in zip(CONTINENTS, CONTINENT_FILLS):
        d.polygon([(mx + px, my + py) for px, py in poly], fill=fill, outline=(150, 144, 120))
    of = F(SANS, 8)
    d.text((mx + 250, my + 52), "ATLANTIC", font=of, fill=(120, 150, 170))
    d.text((mx + 60, my + 52), "PACIFIC", font=of, fill=(120, 150, 170))
    d.text((mx + 700, my + 88), "INDIAN OCEAN", font=of, fill=(120, 150, 170))
    pf = F(SANS_B, 8)
    for num, px, py in PINS:
        cx, cy = mx + px, my + py
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255), width=2)
        label = str(num)
        d.text((cx - d.textlength(label, font=pf) / 2, cy - 5), label, font=pf, fill=(255, 255, 255))
    leg = "EUROPE 5  •  ASIA 2  •  MIDDLE EAST 1  •  NORTH AMERICA 2  •  OCEANIA 2"
    lf = F(SANS_B, 11)
    d.text(((W - d.textlength(leg, font=lf)) / 2, 792), leg, font=lf, fill=INK_SOFT)


# ---------------------------------------------------------------- ALSO list
ALSO = [
    "India v NZ, Test 1 Day 2 — NZ 368, India 159/1 (Jaiswal 85)",
    "Bitcoin below $60,000 — ~$58,300 at Friday's close, lowest since Sep 2024",
    "M5.6 quake hits New Caledonia — no damage, no injuries",
    "Kamala Harris meets Macron in Paris amid 2028 talk",
    "Reuters probe: Epstein, Russia and the oligarchs",
    "Trilateral Peace Declaration: 4 points, no Ukraine deal",
    "ICJ: Myanmar GUILTY of genocide, 9–6 — a first",
    "Anthropic ANT: day one +17% to $97.17; day two −8.5% to $88.91",
    "GTA VI: 32.5m copies, $3.79bn on day one — biggest launch ever",
    "Houthi missile hits PIF Tower in Riyadh; no injuries",
    "Trump pardons Pete Rose posthumously",
    "AMD −7.7% after Hunterbrook report on China",
    "South Africa beat Bangladesh by 9 wickets, top WTC table",
    "UK unveils £260m drone package for Ukraine",
    "Hippo Fiona dies after swallowing a visitor's hat",
    "US Senate rejects Iran war-powers resolution 51–48",
    "EU summons Russian envoy after Kyiv embassy damage",
    "US sanctions Comancheros and 'Ndrangheta",
    "Intuit −10% after hours; sells Mailchimp for $3.68bn",
    "F1 Las Vegas qualifying: Antonelli fastest, but Verstappen on pole",
    "Georgia gas blast: 6 dead, apartment block partly collapses",
    "Israel strikes Hezbollah sites in Lebanon's Bekaa",
    "Canada courts AI data centres as US voters say no",
]


def draw_also(d):
    lab = F(SANS_B, 13)
    d.text((16, 806), "ALSO TODAY", font=lab, fill=INK)
    rule(d, 16, 1008, 824, fill=INK, width=1)
    af = F(SANS, 11)
    col_w = 486
    for i, line in enumerate(ALSO):
        col = 0 if i < 12 else 1
        row = i if i < 12 else i - 12
        x = 16 + col * 506
        y = 830 + row * 12
        d.text((x, y), "▪", font=af, fill=RED)
        d.text((x + 12, y), line, font=af, fill=INK)


# ---------------------------------------------------------------- footer
def draw_footer(d):
    rule(d, 16, 1008, 978, fill=INK, width=1)
    ff = F(SANS, 10)
    d.text((16, 984), "SOURCES: BBC  •  REUTERS  •  CHANNEL NEWS ASIA  •  BLOOMBERG  •  MKT NEWS  •  AP  •  CNN  •  USGS  •  IMD",
           font=ff, fill=INK_SOFT)
    d.text((16, 998), "Compiled Friday 20 November 2026  •  THE FRIDAY GAZETTE",
           font=ff, fill=MUTED)


# ---------------------------------------------------------------- main
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_leads(d)
    draw_tiles(d)
    draw_map(d)
    draw_also(d)
    draw_footer(d)
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "entry.png")
    img.save(out, format="PNG")
    data = open(out, "rb").read()
    print(f"WROTE {out}  {len(data)} bytes  sha256={hashlib.sha256(data).hexdigest()}")
    print(f"SIZE OK: {len(data) <= 1048576}  DIMS: {img.size}")
    return out


if __name__ == "__main__":
    build()
