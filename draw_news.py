#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: a newspaper front page summing up
Wednesday 18 November 2026 in four panels, drawn with Pillow (build time
only; the entry itself is the finished entry.png, copied by main.ts).

Stories (all reported on 18 Nov 2026):
  1. Gulf escalation widens -- Iran fires drones at a US air base in
     Kuwait and targets in Bahrain after the US strike on Qeshm Island;
     Ukraine hits the Kerch bridge a second day and part of its road
     span falls into the strait.
  2. Ebola outbreak in DR Congo more than doubles in three months --
     11,000+ cases, 5,400 deaths; nearly three in four infected
     children under 5 do not survive.
  3. Nvidia doubles revenue to $115.8B and its board rules out
     Jensen Huang's return as CEO.
  4. Democrats win Alaska's Senate seat -- Mary Peltola's victory
     gives the party 56 seats.
"""
import os

from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (24, 28, 38)
NAVY = (18, 38, 66)
RED = (178, 34, 34)
MUTED = (90, 92, 98)

F_BIG = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def cloud(draw, x, y, s, color=(255, 255, 255)):
    draw.ellipse([x, y, x + 70 * s, y + 34 * s], fill=color)
    draw.ellipse([x + 18 * s, y - 16 * s, x + 62 * s, y + 22 * s], fill=color)
    draw.ellipse([x + 42 * s, y - 8 * s, x + 84 * s, y + 30 * s], fill=color)


def panel_text(draw, x, y, w, headline, sub, hl_size=27):
    f_hl = font(F_BIG, hl_size)
    f_sub = font(F_REG, 17)
    lines = wrap(draw, headline, f_hl, w)
    yy = y
    for ln in lines:
        draw.text((x, yy), ln, font=f_hl, fill=INK)
        yy += hl_size + 6
    for ln in wrap(draw, sub, f_sub, w):
        draw.text((x, yy + 4), ln, font=f_sub, fill=MUTED)
        yy += 22


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 86], fill=NAVY)
d.text((28, 16), "WEDNESDAY, 18 NOVEMBER 2026", font=font(F_BIG, 40), fill=(255, 255, 255))
d.text((28, 62), "THE DAY IN FOUR PICTURES  •  WORLD NEWS", font=font(F_REG, 17), fill=(180, 200, 220))

# ---- hero: Gulf escalation at night ----
HX, HY, HW = 24, 102, 976
HH = 452
vgrad(d, (HX, HY, HX + HW, HY + 300), (16, 28, 52), (52, 74, 110))
# stars
for sx, sy, r in [(80, 130, 2), (200, 160, 2), (340, 120, 3), (520, 150, 2),
                  (640, 120, 2), (760, 170, 3), (900, 130, 2), (430, 180, 2)]:
    d.ellipse([HX + sx - r, HY + sy - r, HX + sx + r, HY + sy + r], fill=(255, 255, 255))
# moon
d.ellipse([HX + 830, HY + 36, HX + 900, HY + 106], fill=(240, 232, 200))
# sea
d.rectangle([HX, HY + 300, HX + HW, HY + 330], fill=(20, 48, 78))
for i in range(14):
    d.line([(HX + 30 + i * 70, HY + 314), (HX + 70 + i * 70, HY + 314)], fill=(70, 120, 165), width=3)
# air base on the shore: runway lights + hangars
d.rectangle([HX + 60, HY + 250, HX + 380, HY + 300], fill=(28, 32, 40))
for i in range(8):
    d.ellipse([HX + 80 + i * 38, HY + 270, HX + 88 + i * 38, HY + 278], fill=(255, 200, 60))
d.rectangle([HX + 90, HY + 210, HX + 170, HY + 250], fill=(52, 58, 68))
d.rectangle([HX + 200, HY + 220, HX + 270, HY + 250], fill=(52, 58, 68))
# drone trails arcing in from the right, one intercepted in a flash
d.line([(HX + 940, HY + 120), (HX + 700, HY + 210)], fill=(255, 200, 60), width=4)
d.line([(HX + 960, HY + 180), (HX + 760, HY + 250)], fill=(255, 160, 60), width=4)
d.ellipse([HX + 680, HY + 190, HX + 740, HY + 250], fill=(255, 200, 60))
d.ellipse([HX + 694, HY + 204, HX + 726, HY + 236], fill=(255, 120, 40))
# small drones
for dx, dy in [(HX + 880, HY + 130), (HX + 920, HY + 190)]:
    d.ellipse([dx - 22, dy - 8, dx + 22, dy + 8], fill=(16, 18, 24))
    d.ellipse([dx - 30, dy - 14, dx - 18, dy - 8], fill=(120, 124, 132))
    d.ellipse([dx + 18, dy - 14, dx + 30, dy - 8], fill=(120, 124, 132))
# red banner
d.rectangle([HX + 250, HY + 150, HX + 726, HY + 196], fill=RED)
d.text((HX + 268, HY + 158), "THE GULF IGNITES", font=font(F_BIG, 28), fill=(255, 255, 255))
# hero text block
panel_text(d, HX + 8, HY + 348, HW - 16,
           "Iran's drones reach Kuwait and Bahrain",
           "Tehran widens its attacks after the U.S. strike on Qeshm "
           "Island; Ukraine hits the Kerch bridge a second day.",
           hl_size=36)

# ---- bottom row: three panels ----
BW, GAP = 309, 24
BY = 578
panels = [
    ("EBOLA SURGE IN CONGO", (28, 52, 96), "draw_ebola"),
    ("NVIDIA DOUBLES REVENUE", (30, 90, 120), "draw_chip"),
    ("DEMOCRATS TAKE ALASKA", (58, 48, 92), "draw_vote"),
]
for i, (tag, bg, kind) in enumerate(panels):
    x = 24 + i * (BW + GAP)
    d.rectangle([x, BY, x + BW, BY + 400], fill=(255, 255, 255), outline=(200, 198, 190), width=2)
    d.rectangle([x, BY, x + BW, BY + 34], fill=NAVY)
    d.text((x + 10, BY + 8), tag, font=font(F_BIG, 15), fill=(255, 255, 255))
    ix, iy, iw, ih = x + 2, BY + 36, BW - 4, 168
    if kind == "draw_ebola":
        d.rectangle([ix, iy, ix + iw, iy + ih], fill=(120, 40, 44))
        # clinic tent + virus dots
        d.polygon([(ix + 60, iy + 60), (ix + 150, iy + 60), (ix + 150, iy + 150),
                   (ix + 60, iy + 150)], fill=(245, 240, 230))
        d.polygon([(ix + 40, iy + 66), (ix + 105, iy + 20), (ix + 170, iy + 66)], fill=(200, 60, 60))
        d.rectangle([ix + 98, iy + 84, ix + 112, iy + 126], fill=RED)
        d.rectangle([ix + 84, iy + 98, ix + 126, iy + 112], fill=RED)
        for cx, cy, r in [(ix + 30, iy + 30, 9), (ix + 260, iy + 40, 11),
                          (ix + 280, iy + 130, 8), (ix + 30, iy + 140, 8)]:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 200, 60))
            for dx, dy in [(-r - 5, 0), (r + 5, 0), (0, -r - 5), (0, r + 5)]:
                d.line([(cx, cy), (cx + dx, cy + dy)], fill=(255, 200, 60), width=2)
        panel_text(d, x + 12, BY + 218, BW - 24,
                   "Ebola outbreak more than doubles",
                   "11,000+ cases and 5,400 deaths in DR Congo; nearly "
                   "three in four infected children under 5 die.",
                   hl_size=24)
    elif kind == "draw_chip":
        d.rectangle([ix, iy, ix + iw, iy + ih], fill=(18, 24, 20))
        # green chip with gold pins
        d.rectangle([ix + 84, iy + 34, ix + 220, iy + 134], fill=(24, 110, 60))
        d.rectangle([ix + 104, iy + 54, ix + 200, iy + 114], fill=(16, 70, 40))
        d.text((ix + 122, iy + 72), "AI", font=font(F_BIG, 30), fill=(120, 220, 160))
        for px in range(ix + 96, ix + 210, 22):
            d.line([(px, iy + 20), (px, iy + 34)], fill=(220, 190, 90), width=4)
            d.line([(px, iy + 134), (px, iy + 148)], fill=(220, 190, 90), width=4)
        for py in range(iy + 46, iy + 130, 22):
            d.line([(ix + 70, py), (ix + 84, py)], fill=(220, 190, 90), width=4)
            d.line([(ix + 220, py), (ix + 234, py)], fill=(220, 190, 90), width=4)
        panel_text(d, x + 12, BY + 218, BW - 24,
                   "Nvidia doubles revenue; no Huang return",
                   "Quarterly revenue hits $115.8B; the board rules out "
                   "Jensen Huang coming back as CEO.",
                   hl_size=24)
    else:
        vgrad(d, (ix, iy, ix + iw, iy + ih), (214, 226, 240), (240, 244, 248))
        # capitol dome + ballot box
        d.rectangle([ix + 40, iy + 110, ix + 266, iy + 168], fill=(240, 240, 240))
        d.ellipse([ix + 110, iy + 40, ix + 196, iy + 120], fill=(70, 90, 130))
        d.rectangle([ix + 96, iy + 100, ix + 210, iy + 112], fill=(70, 90, 130))
        for cx in (ix + 70, ix + 120, ix + 170, ix + 220):
            d.rectangle([cx, iy + 122, cx + 12, iy + 168], fill=(180, 190, 200))
        # ballot slip going in
        d.rectangle([ix + 220, iy + 30, ix + 268, iy + 70], fill=(255, 255, 255), outline=(52, 58, 68), width=2)
        d.line([(ix + 228, iy + 58), (ix + 238, iy + 48)], fill=RED, width=4)
        d.line([(ix + 238, iy + 48), (ix + 260, iy + 38)], fill=RED, width=4)
        panel_text(d, x + 12, BY + 218, BW - 24,
                   "Democrats win Alaska's Senate seat",
                   "Mary Peltola's victory gives the party 56 seats — "
                   "capping its rout of the Republicans.",
                   hl_size=24)

# ---- footer ----
d.text((28, 984), "Sources: BBC, AP, CBS, Reuters, UN — Wednesday 18 November 2026",
       font=font(F_REG, 14), fill=MUTED)
d.text((28, 1002), "Also: 6.0 quake in Papua New Guinea · Cyclone Xavier hits Cook Islands · NSA network outage",
       font=font(F_REG, 14), fill=MUTED)

img.save(OUT, optimize=True)
print("saved", img.size)
print(os.path.getsize(OUT), "bytes")
