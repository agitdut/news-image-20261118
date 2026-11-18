#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: a dense single front page summing up
Wednesday 18 November 2026, drawn with Pillow (build time only; the entry
itself is the finished entry.png, copied by main.ts).

Layout (1024x1024): masthead + Gulf lead with a world-at-a-glance map,
Shenzhen summit box, three illustrated features (Kerch bridge, Ebola,
Nvidia), three columns of short items (America / The World / Markets &
Money), a markets strip and an also-in-brief footer. About 27 distinct
stories, every one reported on 18 Nov 2026 (Reuters, AP, BBC, UN News,
Le Monde, ECDC, market closes).

Verified facts used:
  Gulf: US jets hit a Revolutionary Guard missile site on Qeshm Island
    (Tue); Iran then fired drones at Kuwait (Ali al-Salem air base) and
    Bahrain (3rd attack there in a week); Houthi cruise missile towards
    Riyadh destroyed; tanker Tara Gas hit, 24 crew evacuated; Brent ~$93.
  Shenzhen: Xi opened APEC in Shenzhen Wed, talks with Putin; Trump joins
    a three-way meeting Thu; Xi calls for lower trade barriers.
  Kerch: Ukraine hit the Kerch bridge a second day; part of a road span
    fell into the strait; 2 killed; Russia closed road traffic and hit
    bridges in Kyiv in reply.
  Ebola: outbreak more than doubled in 3 months; 11,376 cases, 5,568
    deaths (ECDC, data to 14 Nov); nearly 3 in 4 infected children
    under 5 die; centres Bunia and Beni.
  Nvidia: Q3 revenue $115.8B, up 103% YoY; forecast ~$130B next quarter;
    board chair Harvey Jones: board does not intend to reinstate Jensen
    Huang, who resigned last week; interim CEO Colette Kress.
  Peltola: AP called Alaska for Democrat Mary Peltola over Sen. Dan
    Sullivan; Democrats hold 56 Senate seats from January.
  Shorts: US loses measles elimination status (26 years; 5,400+ cases,
    10 deaths); NSA classified network down Tue, Rubio: no evidence of
    a malign actor; Asif Merchant sentenced to 27 years over a plot to
    kill figures incl. Trump; Waymo pulls driverless taxis off US
    highways after California ban; Trump: "very large" trade deal with
    the Philippines; UK sanctions firms linked to West Bank settlements
    (E1 project); Matan Kahana elected Knesset president, 66 of 120;
    Houthis ~60 km from Aden; thousands protest in Port-au-Prince backing
    Salvadoran troops; Mongolia's president resigns in a railway
    corruption scandal; Costa Rican journalist investigating drug
    trafficking killed; Deutsche Bank leak: 15m internal documents;
    US tightens AI-chip curbs on Southeast Asia, Beijing threatens
    retaliation; UK inflation 3.6% on fuel prices; France protests:
    146,000 by police count; isolated Indigenous group emerges in
    Brazil's Amazon; South Korea offers $75,000 bounties for reporting
    AI cheating in university entrance exams.
  Markets (close 18 Nov): S&P 500 7,340.53 -1.03%, DAX 26,045 -2.08%,
    CAC 40 8,217 -1.62%, FTSE 10,690 -1.76%, Nikkei 59,024 +0.28%,
    Brent $91.55, gold $3,775 -2.31%, VIX 25.46, Bitcoin $64,649.
  Also: Pope Leo XIV in Peru urges no hate; Thailand orders clean water
    over arsenic from Myanmar mines; 16 Ecuadorian fishermen sue the
    Trump administration over their bombed vessel; US soldier suspected
    of spying for Russia handed to US military; ICJ to rule Thu on
    Myanmar/Rohingya genocide case; Amnesty: record political executions
    in Iran.
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
RULE = (190, 186, 176)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
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
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, w, text, fnt, fill, leading, max_lines=None):
    """Draw wrapped text, return y after last line. Raises if it overflows."""
    lines = wrap(draw, text, fnt, w)
    if max_lines is not None and len(lines) > max_lines:
        raise ValueError(f"text overflows ({len(lines)} > {max_lines}): {text[:60]!r}")
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


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


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 24  # margin

# ---- masthead ----
d.rectangle([0, 0, W, 84], fill=NAVY)
d.text((MX, 10), "THE WORLD TODAY", font=font(F_SERIF, 46), fill=(255, 255, 255))
d.text((MX, 62), "WEDNESDAY, 18 NOVEMBER 2026  •  ONE DAY, ONE PAGE  •  WORLD NEWS",
       font=font(F_BIG, 13), fill=(180, 200, 220))

# ---- lead: Gulf (left) + map & Shenzhen (right) ----
LY = 96
# left column
d.text((MX, LY), "WAR IN THE GULF — DAY 3", font=font(F_BIG, 14), fill=RED)
y = block(d, MX, LY + 22, 596, "Iran's drones reach Kuwait and Bahrain",
          font(F_SERIF, 36), INK, 42, max_lines=2)
y = block(d, MX, y + 4, 596,
          "Tehran widens its attacks after US jets struck a Revolutionary "
          "Guard missile site on Qeshm Island; Gulf defences say they "
          "intercepted the drones.",
          font(F_REG, 15), (52, 56, 66), 20, max_lines=3)
y += 8
for b in [
    "Iran says it hit US drone and missile sites at Kuwait's Ali al-Salem base.",
    "Bahrain intercepts Iranian attacks for a third time this week.",
    "Houthi missile at Riyadh destroyed; tanker Tara Gas hit, 24 crew evacuated.",
]:
    d.ellipse([MX + 2, y + 5, MX + 8, y + 11], fill=RED)
    y = block(d, MX + 14, y, 582, b, font(F_REG, 12), (52, 56, 66), 16, max_lines=2)
    y += 3

# right column: world map panel
RX, RW = 644, 356
d.rectangle([RX, LY, RX + RW, LY + 124], fill=(214, 226, 240), outline=(150, 160, 175), width=1)
d.text((RX + 8, LY + 4), "THE WORLD AT A GLANCE", font=font(F_BIG, 11), fill=NAVY)
# schematic continents (equirectangular, coarse but recognisable)
ox, oy = RX + 8, LY + 22
LAND = (168, 178, 158)
d.polygon([(ox + 6, oy + 22), (ox + 30, oy + 6), (ox + 72, oy + 4), (ox + 96, oy + 16),
           (ox + 88, oy + 38), (ox + 60, oy + 52), (ox + 34, oy + 46), (ox + 12, oy + 36)], fill=LAND)  # N America
d.polygon([(ox + 62, oy + 58), (ox + 88, oy + 56), (ox + 92, oy + 78), (ox + 76, oy + 96),
           (ox + 64, oy + 82)], fill=LAND)  # S America
d.polygon([(ox + 158, oy + 8), (ox + 182, oy + 4), (ox + 192, oy + 18), (ox + 178, oy + 32),
           (ox + 160, oy + 28)], fill=LAND)  # Europe
d.polygon([(ox + 158, oy + 36), (ox + 186, oy + 34), (ox + 196, oy + 52), (ox + 184, oy + 78),
           (ox + 168, oy + 72), (ox + 156, oy + 52)], fill=LAND)  # Africa
d.polygon([(ox + 196, oy + 4), (ox + 250, oy + 2), (ox + 300, oy + 10), (ox + 318, oy + 30),
           (ox + 300, oy + 52), (ox + 268, oy + 58), (ox + 238, oy + 44), (ox + 206, oy + 34),
           (ox + 194, oy + 18)], fill=LAND)  # Asia
d.polygon([(ox + 272, oy + 76), (ox + 302, oy + 74), (ox + 306, oy + 88), (ox + 280, oy + 92)],
          fill=LAND)  # Australia
F_MAP = font(F_BIG, 9)
markers = [
    ("KUWAIT", 236, 44, 8, -12), ("KERCH", 208, 22, -34, -12),
    ("SHENZHEN", 292, 44, -14, 12), ("CONGO", 176, 62, -38, 2),
    ("ALASKA", 22, 12, 0, -12),
]
for name, mx, my, dx, dy in markers:
    d.ellipse([ox + mx - 4, oy + my - 4, ox + mx + 4, oy + my + 4], fill=RED,
              outline=(255, 255, 255), width=1)
    d.text((ox + mx + dx, oy + my + dy), name, font=F_MAP, fill=(120, 20, 20))
# Shenzhen box under map
SY = LY + 132
d.rectangle([RX, SY, RX + RW, SY + 92], fill=(255, 255, 255), outline=RULE, width=1)
d.text((RX + 10, SY + 6), "APEC • SHENZHEN", font=font(F_BIG, 11), fill=RED)
block(d, RX + 10, SY + 24, RW - 20, "Xi, Putin and Trump to meet on Thursday",
      font(F_BIG, 17), INK, 21, max_lines=2)
block(d, RX + 10, SY + 66, RW - 20,
      "Xi opens the APEC summit and talks with Putin; Trump joins them tomorrow.",
      font(F_REG, 11), MUTED, 14, max_lines=2)

d.line([(MX, 332), (W - MX, 332)], fill=INK, width=2)

# ---- feature row: three illustrated stories ----
FY = 344
FW, FGAP = 309, 24
features = [
    ("KERCH BRIDGE", "bridge", "Ukraine hits Kerch bridge a second day",
     "Part of a road span falls into the strait; 2 killed. Russia hits bridges in Kyiv in reply."),
    ("EBOLA IN CONGO", "ebola", "Outbreak more than doubles in three months",
     "11,376 cases and 5,568 deaths, the UN says. Nearly 3 in 4 infected children under 5 die."),
    ("NVIDIA", "chip", "Revenue doubles; no return for Huang",
     "Revenue hits $115.8B, up 103%, with ~$130B forecast next. The board will not reinstate Huang."),
]
for i, (tag, kind, hl, sub) in enumerate(features):
    x = MX + i * (FW + FGAP)
    d.rectangle([x, FY, x + FW, FY + 212], fill=(255, 255, 255), outline=RULE, width=1)
    ix, iy, iw, ih = x + 1, FY + 1, FW - 2, 96
    if kind == "bridge":
        vgrad(d, (ix, iy, ix + iw, iy + ih), (232, 196, 150), (250, 222, 190))
        d.rectangle([ix, iy + 62, ix + iw, iy + ih], fill=(44, 92, 130))
        d.rectangle([ix + 40, iy + 20, ix + 52, iy + 78], fill=(70, 76, 86))
        d.rectangle([ix + 256, iy + 20, ix + 268, iy + 78], fill=(70, 76, 86))
        d.rectangle([ix, iy + 62, ix + 118, iy + 74], fill=(52, 58, 68))
        d.rectangle([ix + 190, iy + 62, ix + iw, iy + 74], fill=(52, 58, 68))
        d.polygon([(ix + 118, iy + 62), (ix + 146, iy + 66), (ix + 140, iy + 96),
                   (ix + 124, iy + 92)], fill=(40, 44, 54))
        d.polygon([(ix + 190, iy + 62), (ix + 164, iy + 68), (ix + 170, iy + 94),
                   (ix + 184, iy + 90)], fill=(40, 44, 54))
        cloud(d, ix + 118, iy + 40, 0.7, (120, 118, 116))
        cloud(d, ix + 150, iy + 30, 0.55, (140, 138, 136))
        d.ellipse([ix + 142, iy + 56, ix + 162, iy + 76], fill=(255, 200, 60))
        d.ellipse([ix + 148, iy + 62, ix + 156, iy + 70], fill=(255, 120, 40))
    elif kind == "ebola":
        d.rectangle([ix, iy, ix + iw, iy + ih], fill=(120, 40, 44))
        d.polygon([(ix + 96, iy + 30), (ix + 152, iy + 30), (ix + 152, iy + 96),
                   (ix + 96, iy + 96)], fill=(245, 240, 230))
        d.polygon([(ix + 82, iy + 34), (ix + 124, iy + 6), (ix + 166, iy + 34)], fill=(200, 60, 60))
        d.rectangle([ix + 118, iy + 48, ix + 130, iy + 78], fill=RED)
        for cx, cy, r in [(ix + 40, iy + 26, 9), (ix + 268, iy + 30, 10),
                          (ix + 282, iy + 80, 8), (ix + 34, iy + 82, 8)]:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 200, 60))
            for dx2, dy2 in [(-r - 5, 0), (r + 5, 0), (0, -r - 5), (0, r + 5)]:
                d.line([(cx, cy), (cx + dx2, cy + dy2)], fill=(255, 200, 60), width=2)
    else:
        d.rectangle([ix, iy, ix + iw, iy + ih], fill=(18, 24, 20))
        d.rectangle([ix + 84, iy + 18, ix + 224, iy + 86], fill=(24, 110, 60))
        d.rectangle([ix + 104, iy + 32, ix + 204, iy + 72], fill=(16, 70, 40))
        d.text((ix + 128, iy + 40), "AI", font=font(F_BIG, 26), fill=(120, 220, 160))
        for px in range(ix + 96, ix + 216, 22):
            d.line([(px, iy + 8), (px, iy + 18)], fill=(220, 190, 90), width=4)
            d.line([(px, iy + 86), (px, iy + 96)], fill=(220, 190, 90), width=4)
        for py in range(iy + 30, iy + 80, 22):
            d.line([(ix + 70, py), (ix + 84, py)], fill=(220, 190, 90), width=4)
            d.line([(ix + 224, py), (ix + 238, py)], fill=(220, 190, 90), width=4)
    d.rectangle([x, FY + 98, x + FW, FY + 120], fill=NAVY)
    d.text((x + 10, FY + 104), tag, font=font(F_BIG, 13), fill=(255, 255, 255))
    block(d, x + 10, FY + 126, FW - 20, hl, font(F_BIG, 16), INK, 20, max_lines=2)
    block(d, x + 10, FY + 166, FW - 20, sub, font(F_REG, 11), MUTED, 14, max_lines=2)

d.line([(MX, 568), (W - MX, 568)], fill=INK, width=2)

# ---- three columns of short items ----
CY = 580
COLS = [
    ("AMERICA", [
        ("Peltola wins Alaska; Democrats take 56 seats",
         "AP calls the last undecided race for Peltola."),
        ("US loses measles-free status after 26 years",
         "5,400+ cases and 10 deaths, a first since the 1990s."),
        ("NSA network down in a week of US outages",
         "Rubio: no evidence a malign actor is behind them."),
        ("27 years for plot to kill Trump, others",
         "Asif Merchant sentenced over an assassination plan."),
        ("Waymo pulls driverless taxis off US highways",
         "Move follows a California ban calling them a danger."),
        ("Trump hails “very large” Philippines trade deal",
         "Deal struck as he arrives in the region for APEC."),
    ]),
    ("THE WORLD", [
        ("UK sanctions firms tied to West Bank settlements",
         "London targets builders and the E1 project."),
        ("Kahana elected Knesset president, 66 of 120",
         "A setback for Netanyahu's camp in Israel."),
        ("Houthis now about 60 km from Aden",
         "Their advance puts Yemen's seat of power in reach."),
        ("Thousands march in Haiti backing Salvadoran troops",
         "Crowds in Port-au-Prince thank the anti-gang force."),
        ("Mongolia's president resigns in scandal",
         "Ukhnaa quits over a railway corruption case."),
        ("Journalist investigating drug gangs killed",
         "Costa Rican reporter shot dead by armed men."),
    ]),
    ("MARKETS & MONEY", [
        ("Deutsche Bank leak: 15m internal documents",
         "Papers accuse the bank of ignoring criminal acts."),
        ("US tightens AI-chip curbs on Southeast Asia",
         "Beijing threatens retaliation over the new rules."),
        ("UK inflation rises to 3.6% on fuel prices",
         "Factory costs climb too, stoking rate-hike talk."),
        ("France protests: 146,000 by police count",
         "Cost-of-living marches weaken but stay strong."),
        ("Isolated Indigenous group emerges in Amazon",
         "About 20 people, thin and hungry, leave isolation."),
        ("$75,000 bounties for reporting AI exam cheating",
         "South Korea targets cheats in entrance exams."),
    ]),
]
for i, (sec, items) in enumerate(COLS):
    x = MX + i * (FW + FGAP)
    d.rectangle([x, CY, x + FW, CY + 24], fill=NAVY)
    d.text((x + 10, CY + 5), sec, font=font(F_BIG, 13), fill=(255, 255, 255))
    yy = CY + 32
    for j, (hl, sub) in enumerate(items):
        yy = block(d, x, yy, FW, hl, font(F_BIG, 12), INK, 15, max_lines=2)
        yy = block(d, x, yy + 1, FW, sub, font(F_REG, 10), MUTED, 13, max_lines=1)
        yy += 6
        if j < len(items) - 1:
            d.line([(x, yy - 3), (x + FW, yy - 3)], fill=(220, 218, 210), width=1)

# ---- markets strip ----
MY = 892
d.rectangle([MX, MY, W - MX, MY + 58], fill=(232, 228, 218), outline=RULE, width=1)
d.text((MX + 10, MY + 6), "MARKETS — WEDNESDAY'S CLOSE", font=font(F_BIG, 12), fill=RED)
block(d, MX + 10, MY + 24, W - 2 * MX - 20,
      "S&P 500 7,340.53  −1.03%   •   DAX 26,045  −2.08%   •   CAC 40 8,217  −1.62%   •   FTSE 10,690  −1.76%",
      font(F_BIG, 13), INK, 17, max_lines=1)
block(d, MX + 10, MY + 41, W - 2 * MX - 20,
      "Nikkei 59,024  +0.28%   •   Brent $91.55   •   Gold $3,775  −2.31%   •   VIX 25.46   •   Bitcoin $64,649",
      font(F_BIG, 13), INK, 17, max_lines=1)

# ---- footer: also in brief + sources ----
FY2 = 962
block(d, MX, FY2, W - 2 * MX,
      "ALSO IN BRIEF: Pope Leo XIV urges no hate and no violent language  •  Thailand orders clean water for thousands facing arsenic pollution  •  US soldier suspected of spying for Russia handed to the US military  •  ICJ to rule Thursday on Myanmar's Rohingya case  •  Amnesty: record political executions in Iran.",
      font(F_REG, 11), (52, 56, 66), 14, max_lines=2)
d.text((MX, 1000), "Sources: Reuters, AP, BBC, UN News, Le Monde, ECDC — Wednesday 18 November 2026",
       font=font(F_REG, 11), fill=MUTED)

img.save(OUT, optimize=True)
print("saved", img.size)
print(os.path.getsize(OUT), "bytes")
