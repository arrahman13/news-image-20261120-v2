#!/usr/bin/env python3
"""
build_image.py -- generator for "THE WORLD IN ONE IMAGE", Friday 20 November 2026.

Renders entry.png (1024x1024) deterministically with PIL only: no photos,
no external assets, no randomness, no timestamps. Every illustration
(cyclone spiral, Kyiv night skyline, COP31 draft paper, card icons and the
world map) is drawn programmatically below.

Every story was verified against wire / primary reporting on build day
(Reuters, AP, BBC, Al Jazeera, UN News, IMD via The Hindu BusinessLine,
ESA, ATP, Formula1.com, Sensor Tower via VGC, Dow Jones market data).
Stories that broke on Thursday 19 November are NOT presented as Friday
news; they are listed honestly in the DATE CHECK box.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------
# Canvas and palette (cream broadsheet)
# --------------------------------------------------------------------------
W = H = 1024
CREAM = (250, 246, 236)
PAPER = (253, 251, 244)
INK = (26, 24, 20)
SOFT = (74, 68, 58)
FAINT = (122, 113, 98)
RULE = (38, 34, 28)
HAIR = (196, 188, 168)
RED = (168, 32, 26)
DARKBAR = (30, 28, 24)
GOLD = (176, 132, 40)
TEAL = (24, 92, 104)
NAVY = (16, 24, 48)
SKY = (36, 84, 128)

FD = "/usr/share/fonts/truetype"
SERIF = f"{FD}/liberation/LiberationSerif-Regular.ttf"
SERIF_B = f"{FD}/liberation/LiberationSerif-Bold.ttf"
SERIF_I = f"{FD}/liberation/LiberationSerif-Italic.ttf"
SANS = f"{FD}/liberation/LiberationSans-Regular.ttf"
SANS_B = f"{FD}/liberation/LiberationSans-Bold.ttf"
SANS_I = f"{FD}/liberation/LiberationSans-Italic.ttf"

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def tw(d, s, font):
    return d.textlength(s, font=font)


def wrap(d, s, font, maxw):
    """Greedy word wrap; returns list of lines that fit maxw."""
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def ellip(d, s, font, maxw):
    if tw(d, s, font) <= maxw:
        return s
    while s and tw(d, s + "...", font) > maxw:
        s = s[:-1]
    return s.rstrip() + "..."


def para(d, x, y, s, font, maxw, lh, fill=INK, max_lines=None):
    """Draw wrapped text; returns y after the last line."""
    lines = wrap(d, s, font, maxw)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = ellip(d, lines[-1], font, maxw)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def tag_chip(d, x, y, label):
    """Small claim-status tag; returns width used."""
    f = F(SANS_B, 8)
    w_ = tw(d, label.upper(), f) + 10
    d.rounded_rectangle([x, y, x + w_, y + 13], 3, outline=RED, width=1)
    d.text((x + 5, y + 2), label.upper(), font=f, fill=RED)
    return w_


# --------------------------------------------------------------------------
# Verified content (Friday 20 November 2026)
# --------------------------------------------------------------------------
LEADS = [
    dict(
        n=1, region="Asia-Pacific",
        kicker="GOPALPUR, INDIA - CYCLONE",
        head="Cyclone Akvan comes ashore in Odisha",
        body=("Landfall began at 07:30 IST with winds of 70-80 km/h gusting to 90. "
              "Over 300,000 people were moved into 9,341 shelters; no deaths reported."),
        src="(IMD via The Hindu BusinessLine)", tag="Officials say", art="cyclone",
    ),
    dict(
        n=2, region="Europe",
        kicker="KYIV, UKRAINE - WAR",
        head="Ballistic barrage strikes Kyiv's Dnipro bridges",
        body=("Missiles hit the Podilsko-Voskresenskyi, Darnytskyi and Pivdennyi bridges - "
              "the biggest bridge attack of the war. The mayor reported 3 killed, ~15 injured."),
        src="(Reuters)", tag="Reported", art="kyiv",
    ),
    dict(
        n=3, region="Middle East",
        kicker="ANTALYA, TURKIYE - CLIMATE",
        head="COP31 final day deadlocked on money and fossil fuels",
        body=("The latest draft dropped the fossil-fuel transition pledge and the $120bn-a-year "
              "adaptation confirmation; France and Panama led a bloc demanding a stronger deal."),
        src="(Reuters)", tag="Ongoing", art="cop",
    ),
]

CARDS = [
    dict(n=4, region="Asia-Pacific", icon="chart",
         kicker="TOKYO - SEOUL - TAIPEI - MARKETS",
         head="AI sell-off caps Asia's worst week since 2020",
         body="Nikkei -5.1%, KOSPI -5.2%, Taiex -6.2% Friday; Asia ex-Japan -8.5% on the week. (Reuters)"),
    dict(n=5, region="Asia-Pacific", icon="percent", tag="Forecast",
         kicker="TOKYO, JAPAN - ECONOMY",
         head="Inflation quickens to 2.3% as BoJ hike nears",
         body="Oct CPI +2.3% yr/yr, core +2.2%; 86% of economists expect a Dec hike to 1.50%. (Reuters)"),
    dict(n=6, region="Asia-Pacific", icon="bank",
         kicker="BEIJING, CHINA - ECONOMY",
         head="China holds loan prime rates an 18th month",
         body="One-year LPR kept at 3.00%, five-year at 3.50% in Friday's fixing. (PBoC)"),
    dict(n=7, region="Europe", icon="stars",
         kicker="BRUSSELS - UK-EU",
         head="Reset sealed: food deal and youth mobility",
         body="Food deal from 2028, ETS link, 100k youth places a year by 2030. (Reuters/AP)"),
    dict(n=8, region="Middle East", icon="shield", tag="Reported",
         kicker="BAGHDAD, IRAQ - SECURITY",
         head="Iraqi forces enter Jurf al-Sakhar under deal",
         body="Forces deployed Friday into the Kataib Hezbollah stronghold under a withdrawal deal. (Reuters)"),
    dict(n=9, region="Europe", icon="pill", tag="Reported",
         kicker="BARCELONA - HEALTH",
         head="Cancer pill data: 77% alive at one year",
         body="Daraxonrasib + chemo kept 77% of 61 pancreatic patients alive at 1 year. (Company data, ENA)"),
    dict(n=10, region="Europe", icon="placard", tag="Reported",
         kicker="ROME, ITALY - LABOUR",
         head="General strike shuts Italy down for a day",
         body="CGIL's day-long strike drew protests in 100+ cities; union claims 1m+ took part. (Reuters)"),
    dict(n=11, region="Oceania", icon="cricket",
         kicker="WELLINGTON - CRICKET",
         head="Phillips' 118 headlines New Zealand's day",
         body="Phillips 118, Nicholls 175* as NZ made 368; India closed day two on 159-1. (Reuters)"),
    dict(n=12, region="Americas", icon="gamepad", tag="Estimate",
         kicker="UNITED STATES - GAMING",
         head="GTA VI day-one sales estimated at $2.36bn",
         body="Sensor Tower: 24.58m copies, $2.36bn on day one - above 'Avatar' box office. (VGC)"),
    dict(n=13, region="Europe", icon="missile", tag="Officials say",
         kicker="POLAND - WAR",
         head="Russian missile and drone fall in Poland",
         body="Defence minister confirmed two missiles and a jet drone came down in Poland. (Reuters)"),
    dict(n=14, region="Americas", icon="flag",
         kicker="LAS VEGAS - FORMULA 1",
         head="Russell fastest in wet Vegas practice",
         body="Russell topped FP2 in 1:47.272 on a rain-hit night session, ahead of Norris. (Formula1.com)"),
]

BRIEFS = [
    (15, "Europe", "Kharkiv: drone strike hits a hospital, injuring four. (Reuters)"),
    (16, "Europe", "Kryvyi Rih power cut; Ukraine toll 8 killed, 28 injured. (Times)"),
    (17, "Asia-Pacific", "Seoul: 111 Suneung candidates caught with banned devices. (BBC)"),
    (18, "Middle East", "Hormuz: crude shipments near pre-war levels; Brent steady. (Reuters)"),
    (19, "Africa", "Malawi: petrol $3.24/litre, Africa's dearest; violent queues. (AJ/AFP)"),
    (20, "World/Space", "BepiColombo reaches Mercury after 8-year, ~10bn-km cruise. (ESA)"),
    (21, "Europe", "Turin: Alcaraz-Cobolli, Medvedev-Tiafoe for last SF place. (ATP)"),
    (22, "Asia-Pacific", "Odisha: 209mm rain at Patrapur; landfall done by 11:20 IST. (IMD)"),
    (23, "Europe", "Ukraine: 404 drones, ~100 missiles overnight; 23 sites hit. (Officials)"),
    (24, "Americas", "Las Vegas: Friday-night qualifying after Russell's FP2 pace. (F1)"),
    (25, "Asia-Pacific", "Nikkei closes at 56,437 as SoftBank leads Tokyo's rout. (Reuters)"),
    (26, "Middle East", "Turkiye announces $26bn in side deals struck at COP31. (Reuters)"),
    (27, "Europe", "Panama threatens formal objection over weak COP31 text. (UN News)"),
    (28, "Oceania", "Nicholls' unbeaten 175 anchors NZ's 368 in Wellington. (Reuters)"),
    (29, "Asia-Pacific", "Taiex ends week -17.5%, its worst week since 1990. (Reuters)"),
    (30, "Europe", "UK-EU tuition-fee talks given a six-month deadline. (Reuters)"),
    (31, "World/Space", "Nine flybys in eight years: BepiColombo's road to Mercury. (ESA)"),
    (32, "Middle East", "Brent heads for a third straight weekly decline. (Reuters)"),
    (33, "Asia-Pacific", "Akvan weakens over land; still no deaths reported. (IMD)"),
    (34, "Europe", "Dnipropetrovsk region: one killed, five injured. (Reuters)"),
    (35, "World/Space", "Gold falls 2% to $3,552.20/oz in the global rout. (Reuters)"),
    (36, "Europe", "Italy rail strike begins 21:00 Friday, into Saturday. (Reuters)"),
    (37, "Asia-Pacific", "Hang Seng closes -1.9% at 22,411, an 18-month low. (Dow Jones)"),
]

STATS = [
    ("300,000+", "evacuated ahead of Cyclone Akvan (officials)"),
    ("404", "drones in Russia's overnight barrage (Ukr. Air Force)"),
    ("-17.5%", "Taiex this week - worst since 1990 (Reuters)"),
    ("2.3%", "Japan Oct CPI, yr/yr (Statistics Bureau)"),
    ("118", "Glenn Phillips' century vs India (Reuters)"),
    ("8 yrs", "BepiColombo's cruise to Mercury (ESA)"),
]

# Hour-by-hour UTC timeline: (utc_hour, label, approx?, label row)
# rows: af = above-far, an = above-near, bn = below-near, bf = below-far
TIMELINE = [
    (1.0, "01:00 China LPR held", False, "af"),
    (1.5, "~01:30 Kyiv bridges hit", True, "bn"),
    (2.5, "02:30 Akvan landfall", False, "an"),
    (4.0, "04:00 FP2 Vegas", False, "bf"),
    (6.0, "06:00 Nikkei -5.1%", False, "bf"),
    (6.5, "06:30 KOSPI -5.2%", False, "an"),
    (8.0, "08:00 Hang Seng -1.9%", False, "bn"),
    (9.0, "09:00 Brent $91.03", False, "an"),
    (20.0, "20:00 Italy rail strike", False, "bn"),
]

MARKETS = [
    ("NIKKEI", "-5.1%"), ("KOSPI", "-5.2%"), ("TAIEX", "-6.2%"),
    ("HANG SENG", "-1.9%"), ("BRENT", "$92.22 +0.3%"), ("GOLD", "$3,552 -2%"),
]

WHATS_NEXT = [
    "Sat 21 Nov - BepiColombo Mercury orbit insertion (ESA)",
    "Sat 21 Nov - ATP Finals semi-finals, Turin",
    "Sat night 21 Nov - Las Vegas Grand Prix race",
    "Weekend 21-22 Nov - COP31 talks may overrun",
]

DATE_CHECK = [
    "Shenzhen summit: Trump-Xi-Putin met THURSDAY.",
    "Anthropic IPO: priced THURSDAY; Friday was fallout.",
    "ICJ Rohingya verdict: delivered THURSDAY, The Hague.",
    "GTA VI launch: THURSDAY night (estimate is #12).",
    "Fiona the hippo: death announced THURSDAY.",
    "Bukele filing: late THURSDAY; Friday was reaction.",
]


# --------------------------------------------------------------------------
# Programmatic illustrations for the three lead panels
# --------------------------------------------------------------------------
def art_cyclone(d, x, y, w_, h):
    """Spiral storm over a simplified Bay of Bengal / Odisha coast."""
    d.rectangle([x, y, x + w_, y + h], fill=(198, 222, 228))
    # land mass (Odisha coast) along the top-left
    d.polygon([(x, y), (x + w_ * 0.52, y), (x + w_ * 0.44, y + h * 0.30),
               (x + w_ * 0.30, y + h * 0.46), (x + w_ * 0.10, y + h * 0.52),
               (x, y + h * 0.60)], fill=(214, 199, 152), outline=(150, 132, 84))
    d.text((x + 8, y + 5), "ODISHA", font=F(SANS_B, 9), fill=(110, 92, 48))
    d.text((x + w_ - 74, y + h - 15), "BAY OF BENGAL", font=F(SANS_I, 8), fill=SKY)
    cx, cy = x + w_ * 0.58, y + h * 0.58
    # spiral arms
    for k in range(3):
        pts = []
        for t in range(0, 101):
            a = k * 2.094 + t / 100 * 4.6
            r = 4 + t / 100 * min(w_, h) * 0.46
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.82))
        d.line(pts, fill=(255, 255, 255), width=5)
        d.line(pts, fill=(120, 160, 175), width=1)
    d.ellipse([cx - 9, cy - 8, cx + 9, cy + 8], fill=(240, 248, 250), outline=TEAL, width=2)
    # rain streaks
    for i in range(9):
        rx = x + 12 + i * (w_ - 24) / 8
        d.line([(rx, y + h - 13), (rx - 5, y + h - 4)], fill=SKY, width=2)
    # landfall marker near Gopalpur
    gx, gy = x + w_ * 0.335, y + h * 0.475
    d.line([(gx - 7, gy), (gx + 7, gy)], fill=RED, width=2)
    d.line([(gx, gy - 7), (gx, gy + 7)], fill=RED, width=2)
    d.text((gx + 9, gy - 5), "GOPALPUR", font=F(SANS_B, 8), fill=RED)


def art_kyiv(d, x, y, w_, h):
    """Night skyline, a bridge over the river, missile trails and bursts."""
    d.rectangle([x, y, x + w_, y + h], fill=NAVY)
    # stars
    for sx, sy in [(0.08, 0.15), (0.22, 0.08), (0.38, 0.2), (0.55, 0.1),
                   (0.7, 0.18), (0.85, 0.07), (0.93, 0.22), (0.47, 0.05)]:
        d.point((x + sx * w_, y + sy * h), fill=(220, 226, 240))
    ground = y + h * 0.78
    # skyline silhouettes
    bx = x + 6
    for bw, bh in [(26, 30), (18, 42), (30, 23), (16, 35), (24, 26), (20, 45), (28, 21), (18, 33)]:
        d.rectangle([bx, ground - bh, bx + bw, ground], fill=(8, 12, 26))
        for wy in range(int(ground - bh) + 5, int(ground) - 4, 8):
            d.point((bx + bw // 2, wy), fill=(250, 205, 90))
        bx += bw + 5
    # river + bridge
    d.rectangle([x, ground, x + w_, y + h], fill=(22, 44, 74))
    d.arc([x + w_ * 0.30, ground - 24, x + w_ * 0.86, ground + 20], 180, 360, fill=(200, 210, 225), width=2)
    d.line([(x + w_ * 0.30, ground), (x + w_ * 0.86, ground)], fill=(200, 210, 225), width=2)
    # missile trails (arcs descending) with warhead dots and bursts
    trails = [(0.06, 0.05, 0.40, 0.62), (0.30, 0.02, 0.58, 0.60), (0.62, 0.04, 0.80, 0.58)]
    for sx, sy, ex, ey in trails:
        pts = []
        for t in range(0, 41):
            u = t / 40
            px = x + (sx + (ex - sx) * u) * w_
            py = y + (sy + (ey - sy) * u * u + 0.18 * u * (1 - u)) * h
            pts.append((px, py))
        d.line(pts, fill=(255, 170, 60), width=2)
        hx, hy = pts[-1]
        d.ellipse([hx - 3, hy - 3, hx + 3, hy + 3], fill=(255, 230, 160))
        for a in range(0, 360, 45):
            d.line([(hx, hy), (hx + 9 * math.cos(math.radians(a)), hy + 9 * math.sin(math.radians(a)))],
                   fill=(255, 120, 50), width=1)
    d.text((x + 8, y + h - 14), "DNIPRO RIVER", font=F(SANS_I, 8), fill=(150, 175, 205))


def art_cop(d, x, y, w_, h):
    """A draft deal sheet with lines struck through in red."""
    d.rectangle([x, y, x + w_, y + h], fill=(233, 226, 205))
    px, py, pw, ph = x + w_ * 0.15, y + 5, w_ * 0.56, h - 10
    d.rectangle([px + 4, py + 4, px + pw + 4, py + ph + 4], fill=(178, 168, 140))
    d.rectangle([px, py, px + pw, py + ph], fill=(253, 252, 246), outline=(150, 140, 115))
    d.text((px + 9, py + 5), "COP31 DRAFT DEAL", font=F(SANS_B, 9.5), fill=INK)
    ly = py + 20
    for i, wd in enumerate([0.86, 0.78, 0.82]):
        d.line([(px + 9, ly), (px + 9 + (pw - 18) * wd, ly)], fill=(150, 148, 138), width=3)
        if i == 1:
            d.line([(px + 5, ly), (px + pw - 5, ly)], fill=RED, width=2)
        ly += 8
    d.text((px + 9, ly + 1), "$120bn/yr dropped", font=F(SANS_B, 8.5), fill=RED)
    # gavel
    gx, gy = x + w_ * 0.80, y + h * 0.26
    d.line([(gx, gy), (gx + 24, gy + 24)], fill=(120, 82, 40), width=4)
    d.rectangle([gx - 12, gy - 12, gx + 8, gy + 2], fill=(146, 102, 50), outline=(96, 64, 26))
    d.rectangle([x + w_ * 0.76, y + h * 0.70, x + w_ * 0.94, y + h * 0.76], fill=(120, 82, 40))


# --------------------------------------------------------------------------
# Small card icons (drawn in a ~30x30 box)
# --------------------------------------------------------------------------
def icon(d, kind, x, y, s=30):
    cx, cy = x + s / 2, y + s / 2
    if kind == "chart":
        pts = [(x + 3, y + 7), (x + 11, y + 12), (x + 18, y + 10), (x + 27, y + 22)]
        d.line(pts, fill=RED, width=3)
        d.polygon([(x + 27, y + 22), (x + 21, y + 21), (x + 26, y + 16)], fill=RED)
        d.line([(x + 3, y + s - 3), (x + s - 3, y + s - 3)], fill=FAINT, width=1)
    elif kind == "percent":
        d.text((x + 5, y + 3), "%", font=F(SANS_B, 24), fill=TEAL)
    elif kind == "bank":
        d.polygon([(x + 3, y + 10), (x + s / 2, y + 3), (x + s - 3, y + 10)], fill=GOLD)
        for i in range(3):
            bx = x + 6 + i * 8
            d.rectangle([bx, y + 13, bx + 4, y + 24], fill=GOLD)
        d.rectangle([x + 3, y + 26, x + s - 3, y + 28], fill=GOLD)
    elif kind == "stars":
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=(36, 62, 140), width=2)
        for a in range(0, 360, 60):
            sx = cx + 8 * math.cos(math.radians(a))
            sy = cy + 8 * math.sin(math.radians(a))
            d.polygon([(sx, sy - 3), (sx + 2.4, sy + 2), (sx - 2.4, sy + 2)], fill=GOLD)
    elif kind == "shield":
        d.polygon([(cx, y + 3), (x + s - 4, y + 8), (x + s - 4, y + 18),
                   (cx, y + s - 3), (x + 4, y + 18), (x + 4, y + 8)], outline=TEAL, width=2)
        d.line([(cx - 5, cy), (cx - 1, cy + 4), (cx + 6, cy - 4)], fill=TEAL, width=2)
    elif kind == "pill":
        d.rounded_rectangle([x + 4, y + 10, x + s - 4, y + 20], 7, outline=RED, width=2)
        d.line([(cx, y + 10), (cx, y + 20)], fill=RED, width=2)
        d.line([(x + 7, y + 24), (x + 13, y + 24)], fill=FAINT, width=2)
        d.line([(x + 17, y + 24), (x + 23, y + 24)], fill=FAINT, width=2)
    elif kind == "placard":
        d.rectangle([x + 5, y + 4, x + s - 5, y + 17], outline=INK, width=2)
        d.line([(x + 8, y + 9), (x + s - 8, y + 9)], fill=RED, width=2)
        d.line([(x + 8, y + 13), (x + s - 11, y + 13)], fill=INK, width=2)
        d.line([(cx, y + 17), (cx, y + s - 3)], fill=INK, width=2)
    elif kind == "cricket":
        d.polygon([(x + 7, y + 3), (x + 12, y + 3), (x + 12, y + 20), (x + 7, y + 20)],
                  fill=(196, 160, 92), outline=(130, 100, 55))
        d.line([(x + 9.5, y + 20), (x + 9.5, y + 26)], fill=(130, 100, 55), width=2)
        d.ellipse([x + 18, y + 17, x + 27, y + 26], fill=RED)
    elif kind == "gamepad":
        d.rounded_rectangle([x + 3, y + 9, x + s - 3, y + 23], 7, outline=INK, width=2)
        d.line([(x + 9, y + 13), (x + 9, y + 19)], fill=INK, width=2)
        d.line([(x + 6, y + 16), (x + 12, y + 16)], fill=INK, width=2)
        d.ellipse([x + 20, y + 12, x + 23, y + 15], fill=RED)
        d.ellipse([x + 20, y + 17, x + 23, y + 20], fill=TEAL)
    elif kind == "missile":
        d.polygon([(x + 20, y + 4), (x + 26, y + 10), (x + 14, y + 22), (x + 9, y + 17)],
                  fill=SOFT, outline=INK)
        d.polygon([(x + 9, y + 17), (x + 5, y + 26), (x + 13, y + 24)], fill=(255, 150, 50))
        d.line([(x + 6, y + 27), (x + 3, y + 29)], fill=RED, width=2)
    elif kind == "flag":
        for r in range(3):
            for c in range(4):
                if (r + c) % 2 == 0:
                    d.rectangle([x + 4 + c * 6, y + 6 + r * 6, x + 10 + c * 6, y + 12 + r * 6], fill=INK)
        d.line([(x + 4, y + 4), (x + 4, y + s - 2)], fill=INK, width=2)
    else:
        d.ellipse([x + 6, y + 6, x + s - 6, y + s - 6], outline=FAINT, width=2)


# --------------------------------------------------------------------------
# Simplified world map (equirectangular, hand-drawn continent polygons)
# --------------------------------------------------------------------------
def lonlat_to_xy(lon, lat, x, y, w_, h):
    return x + (lon + 180) / 360 * w_, y + (90 - lat) / 180 * h


CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 70), (-85, 66), (-80, 62),
     (-76, 58), (-65, 50), (-55, 47), (-65, 44), (-70, 42), (-74, 39), (-76, 35),
     (-80, 32), (-81, 26), (-84, 30), (-89, 30), (-94, 29), (-97, 26), (-97, 22),
     (-94, 18), (-90, 14), (-83, 9), (-79, 9), (-86, 13), (-92, 15), (-105, 20),
     (-110, 24), (-114, 29), (-117, 33), (-122, 37), (-124, 46), (-130, 54), (-150, 60)],
    # South America
    [(-79, 9), (-72, 12), (-64, 10), (-52, 5), (-50, 0), (-44, -3), (-35, -8),
     (-39, -13), (-40, -21), (-48, -26), (-57, -34), (-62, -39), (-65, -41),
     (-65, -45), (-67, -50), (-69, -52), (-71, -54), (-73, -50), (-73, -44),
     (-73, -37), (-71, -30), (-70, -20), (-75, -15), (-79, -8), (-81, -4), (-80, 1), (-77, 4)],
    # Europe
    [(-9, 43), (-9, 37), (-2, 37), (3, 42), (7, 44), (10, 44), (12, 42), (16, 40),
     (18, 40), (15, 44), (19, 46), (23, 40), (26, 38), (23, 36), (28, 41), (30, 46),
     (28, 45), (32, 47), (38, 47), (40, 52), (32, 55), (28, 59), (21, 60), (18, 56),
     (21, 65), (25, 66), (31, 70), (18, 69), (12, 65), (5, 60), (5, 58), (8, 57),
     (10, 59), (18, 59), (20, 55), (14, 54), (8, 54), (3, 53), (0, 51), (-2, 50),
     (-5, 48), (-2, 44), (-9, 43)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (33, 27), (35, 24),
     (38, 20), (40, 15), (43, 12), (48, 11), (51, 10), (46, 5), (41, -2), (40, -10),
     (39, -18), (36, -22), (33, -26), (28, -33), (20, -35), (17, -32), (15, -27),
     (13, -18), (12, -12), (13, -6), (9, -1), (9, 4), (4, 6), (-3, 5), (-8, 4),
     (-13, 8), (-17, 12), (-17, 15), (-16, 20), (-15, 25), (-13, 28), (-10, 31), (-6, 35)],
    # Asia (incl. Middle East, India, SE Asia)
    [(30, 46), (38, 47), (48, 46), (60, 46), (70, 48), (85, 48), (100, 50), (115, 50),
     (130, 48), (140, 48), (142, 52), (142, 59), (155, 60), (170, 66), (178, 65),
     (170, 60), (158, 52), (145, 45), (140, 40), (135, 35), (129, 33), (122, 31),
     (120, 25), (110, 20), (108, 15), (106, 9), (103, 5), (100, 8), (98, 14),
     (95, 16), (92, 15), (89, 22), (88, 21), (85, 19), (80, 15), (77, 8), (73, 16),
     (72, 20), (68, 23), (66, 25), (61, 25), (57, 26), (52, 26), (50, 29), (48, 30),
     (50, 25), (55, 24), (58, 22), (55, 17), (52, 15), (45, 12), (43, 12), (40, 15),
     (39, 20), (35, 28), (36, 36), (30, 36), (27, 37), (30, 41), (33, 42), (36, 42),
     (30, 46)],
    # Indonesia / Papua (simple chain)
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -9), (125, -10),
     (131, -3), (136, -2), (141, -3), (146, -6), (147, -9), (141, -8), (136, -4),
     (130, -4), (125, -9), (118, -10), (110, -8), (102, -4), (97, 2), (95, 5)],
    # Australia
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (130, -32),
     (133, -32), (136, -35), (139, -37), (145, -38), (150, -37), (153, -30),
     (153, -25), (151, -24), (146, -19), (143, -15), (142, -11), (140, -17),
     (136, -15), (135, -12), (132, -11), (130, -12), (126, -14), (122, -17),
     (118, -20), (114, -21), (113, -22)],
    # New Zealand
    [(167, -45), (171, -42), (173, -39), (176, -38), (178, -37), (176, -40),
     (174, -41), (172, -43), (169, -46), (167, -45)],
]

PINS = [  # story number, lon, lat
    (1, 86.4, 20.1), (2, 30.5, 50.4), (3, 30.7, 36.9), (4, 139.7, 35.7),
    (5, 141.5, 37.5), (6, 116.4, 39.9), (7, 4.3, 50.8), (8, 44.4, 33.3),
    (9, 2.2, 41.4), (10, 12.5, 41.9), (11, 174.8, -41.3), (12, -74.0, 40.7),
    (13, 19.0, 52.0), (14, -115.1, 36.2),
]


def draw_map(d, x, y, w_, h):
    d.rectangle([x, y, x + w_, y + h], fill=(226, 234, 236), outline=HAIR)
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, x, y, w_, h) for lon, lat in poly]
        d.polygon(pts, fill=(206, 198, 168), outline=(150, 140, 110))
    for n, lon, lat in PINS:
        px, py = lonlat_to_xy(lon, lat, x, y, w_, h)
        r = 8 if n <= 3 else 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
        label = str(n)
        f = F(SANS_B, 9 if n < 10 else 8)
        d.text((px - tw(d, label, f) / 2, py - 5), label, font=f, fill=(255, 255, 255))
    # Mercury callout (story 20)
    mx, my = x + w_ - 30, y + 22
    d.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=(168, 148, 128), outline=(120, 104, 84))
    d.ellipse([mx - 4, my - 3, mx + 1, my + 2], outline=(120, 104, 84))
    d.ellipse([mx - 7.5, my - 7.5, mx + 7.5, my + 7.5], fill=RED, outline=(255, 255, 255), width=1)
    d.text((mx - 6, my - 5), "20", font=F(SANS_B, 8), fill=(255, 255, 255))
    d.text((mx - 30, my + 14), "MERCURY", font=F(SANS_B, 7), fill=SOFT)


# --------------------------------------------------------------------------
# Page assembly
# --------------------------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    MX = 24                      # side margin
    CW = W - 2 * MX              # content width = 976

    # ---- masthead ---------------------------------------------------------
    d.line([(MX, 10), (W - MX, 10)], fill=RULE, width=3)
    d.line([(MX, 15), (W - MX, 15)], fill=RULE, width=1)
    d.text((MX, 21), "THE WORLD IN ONE IMAGE  -  A ONE-PAGE BROADSHEET OF THE DAY",
           font=F(SANS_B, 11), fill=SOFT)
    d.text((W - MX - tw(d, "No. 20261120 - V2", F(SANS, 11)), 21), "No. 20261120 - V2",
           font=F(SANS, 11), fill=SOFT)
    title = "Friday 20 November 2026"
    tf = F(SERIF_B, 52)
    d.text(((W - tw(d, title, tf)) / 2, 34), title, font=tf, fill=INK)
    d.line([(MX, 90), (W - MX, 90)], fill=RULE, width=1)
    d.line([(MX, 94), (W - MX, 94)], fill=RULE, width=3)

    # ---- sub-headline strip ----------------------------------------------
    d.rectangle([MX, 100, W - MX, 120], fill=DARKBAR)
    sub = ("AKVAN ASHORE IN ODISHA  -  KYIV'S BRIDGES HIT  -  COP31 DEADLOCKED IN ANTALYA  -  "
           "ASIA'S WORST WEEK SINCE 2020")
    sf = F(SANS_B, 12)
    d.text(((W - tw(d, sub, sf)) / 2, 104), sub, font=sf, fill=(248, 244, 232))

    # ---- stat strip --------------------------------------------------------
    sy = 126
    colw = CW / 6
    for i, (num, cap) in enumerate(STATS):
        cx = MX + i * colw
        nf = F(SERIF_B, 25)
        d.text((cx + (colw - tw(d, num, nf)) / 2, sy), num, font=nf, fill=INK)
        cf = F(SANS, 9)
        lines = wrap(d, cap, cf, colw - 10)
        ly = sy + 30
        for ln in lines[:2]:
            d.text((cx + (colw - tw(d, ln, cf)) / 2, ly), ln, font=cf, fill=SOFT)
            ly += 10.5
        if i:
            d.line([(cx, sy + 2), (cx, sy + 44)], fill=HAIR, width=1)
    d.line([(MX, 180), (W - MX, 180)], fill=HAIR, width=1)

    # ---- region tally bar ---------------------------------------------------
    ry = 186
    tally = {}
    for s in LEADS + CARDS:
        tally[s["region"]] = tally.get(s["region"], 0) + 1
    for _, rg, _ in BRIEFS:
        tally[rg] = tally.get(rg, 0) + 1
    order = ["Europe", "Americas", "Asia-Pacific", "Middle East", "Africa", "Oceania", "World/Space"]
    parts = [f"{r} {tally.get(r, 0)}" for r in order]
    total = sum(tally.values())
    tally_txt = "WHERE THE NEWS WAS:  " + "  -  ".join(parts) + f"   =   {total} STORIES"
    d.rectangle([MX, ry, W - MX, ry + 19], fill=(238, 232, 214))
    rf = F(SANS_B, 11.5)
    d.text(((W - tw(d, tally_txt, rf)) / 2, ry + 3.5), tally_txt, font=rf, fill=INK)

    # ---- hour-by-hour UTC timeline ------------------------------------------
    ty = 212
    d.text((MX, ty), "FRIDAY, HOUR BY HOUR (UTC)", font=F(SANS_B, 11), fill=INK)
    axis_y = ty + 43
    row_y = {"af": ty + 12, "an": ty + 23, "bn": axis_y + 6, "bf": axis_y + 17}
    x0, x1 = MX + 6, W - MX - 6
    d.line([(x0, axis_y), (x1, axis_y)], fill=RULE, width=2)
    for hr in range(0, 25, 4):
        hx = x0 + (x1 - x0) * hr / 24
        d.line([(hx, axis_y - 3), (hx, axis_y + 3)], fill=RULE, width=1)
        lab = f"{hr:02d}:00"
        d.text((hx - tw(d, lab, F(SANS, 8)) / 2, axis_y + 28), lab, font=F(SANS, 8), fill=FAINT)
    for hr, lab, approx, row in TIMELINE:
        hx = x0 + (x1 - x0) * hr / 24
        d.ellipse([hx - 4, axis_y - 4, hx + 4, axis_y + 4], fill=RED if approx else TEAL,
                  outline=(255, 255, 255), width=1)
        ly = row_y[row]
        if row in ("af", "an"):
            d.line([(hx, axis_y - 5), (hx, ly + 10)], fill=FAINT, width=1)
        else:
            d.line([(hx, axis_y + 5), (hx, ly - 1)], fill=FAINT, width=1)
        lf = F(SANS, 8.5)
        tx = min(max(hx - tw(d, lab, lf) / 2, MX), W - MX - tw(d, lab, lf))
        d.text((tx, ly), lab, font=lf, fill=INK)
    d.line([(MX, ty + 82), (W - MX, ty + 82)], fill=HAIR, width=1)

    # ---- lead panels ----------------------------------------------------------
    ly0 = ty + 90
    lh = 180
    lw = (CW - 16) / 3
    arts = {"cyclone": art_cyclone, "kyiv": art_kyiv, "cop": art_cop}
    for i, s in enumerate(LEADS):
        px = MX + i * (lw + 8)
        d.rectangle([px, ly0, px + lw, ly0 + lh], fill=PAPER, outline=RULE, width=1)
        arts[s["art"]](d, px + 5, ly0 + 5, lw - 10, 64)
        ky = ly0 + 74
        d.text((px + 8, ky), f"{s['n']}  -  {s['kicker']}", font=F(SANS_B, 9), fill=RED)
        hy = para(d, px + 8, ky + 12, s["head"], F(SERIF_B, 14.5), lw - 16, 16.5, max_lines=2)
        by = para(d, px + 8, hy + 2, s["body"], F(SANS, 9.5), lw - 16, 11.5, max_lines=3)
        d.text((px + 8, by + 1), s["src"], font=F(SANS_I, 8.5), fill=SOFT)
        if s.get("tag"):
            tag_chip(d, px + lw - 8 - (tw(d, s["tag"].upper(), F(SANS_B, 8)) + 10), ly0 + lh - 18, s["tag"])

    # ---- cards grid ------------------------------------------------------------
    cy0 = ly0 + lh + 8
    chh = 84
    cwid = (CW - 24) / 4
    for idx, c in enumerate(CARDS):
        r, col = divmod(idx, 4)
        px = MX + col * (cwid + 8)
        py = cy0 + r * (chh + 6)
        d.rectangle([px, py, px + cwid, py + chh], fill=PAPER, outline=HAIR, width=1)
        icon(d, c["icon"], px + 5, py + 6, 30)
        tx = px + 40
        d.text((tx, py + 5), f"{c['n']} - {c['kicker']}", font=F(SANS_B, 7.5), fill=RED)
        hy = para(d, tx, py + 15, c["head"], F(SERIF_B, 11.5), px + cwid - tx - 6, 13.5, max_lines=2)
        para(d, tx, hy + 2, c["body"], F(SANS, 8.5), px + cwid - tx - 6, 10.5, max_lines=2)
        if c.get("tag"):
            tag_chip(d, px + 6, py + chh - 16, c["tag"])

    # ---- bottom band: map + what's next | briefs + date check -------------------
    by0 = cy0 + 3 * chh + 2 * 6 + 8
    left_w = 330
    d.text((MX, by0), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=INK)
    draw_map(d, MX, by0 + 16, left_w, 108)
    wy = by0 + 128
    d.rectangle([MX, wy, MX + left_w, wy + 60], fill=(238, 232, 214), outline=RULE, width=1)
    d.text((MX + 8, wy + 5), "WHAT'S NEXT", font=F(SANS_B, 10.5), fill=RED)
    for j, item in enumerate(WHATS_NEXT):
        d.text((MX + 8, wy + 20 + j * 10.5), "- " + item, font=F(SANS, 9), fill=INK)

    bx = MX + left_w + 14
    bw = W - MX - bx
    d.text((bx, by0), "ALSO ON FRIDAY", font=F(SANS_B, 11), fill=INK)
    col_w = (bw - 12) / 2
    per_col = (len(BRIEFS) + 1) // 2
    for j, (n, _rg, txt) in enumerate(BRIEFS):
        col = 0 if j < per_col else 1
        row = j if col == 0 else j - per_col
        tx = bx + col * (col_w + 12)
        tyy = by0 + 16 + row * 10.8
        d.text((tx, tyy), f"{n}.", font=F(SANS_B, 8.5), fill=RED)
        d.text((tx + 17, tyy), ellip(d, txt, F(SANS, 8.5), col_w - 18), font=F(SANS, 8.5), fill=INK)

    dy = by0 + 152
    d.rectangle([bx, dy, bx + bw, dy + 48], outline=RED, width=2)
    d.text((bx + 8, dy + 4), "DATE CHECK - BIG STORIES THAT ARE NOT FRIDAY NEWS (THEY BROKE THURSDAY 19 NOV)",
           font=F(SANS_B, 9.5), fill=RED)
    for j, item in enumerate(DATE_CHECK):
        col = j % 2
        row = j // 2
        tx = bx + 8 + col * (bw / 2)
        d.text((tx, dy + 18 + row * 10.5), "- " + ellip(d, item, F(SANS, 8), bw / 2 - 14),
               font=F(SANS, 8), fill=INK)

    # ---- markets strip ---------------------------------------------------------
    my = dy + 56
    d.rectangle([MX, my, W - MX, my + 20], fill=DARKBAR)
    seg = "MARKETS (FRI CLOSE):   " + "    ".join(f"{k} {v}" for k, v in MARKETS) + "   (Reuters / Dow Jones)"
    mf = F(SANS_B, 11)
    d.text(((W - tw(d, seg, mf)) / 2, my + 4), seg, font=mf, fill=(248, 244, 232))

    # ---- footer ------------------------------------------------------------------
    fy = my + 26
    d.line([(MX, fy), (W - MX, fy)], fill=RULE, width=1)
    foot = "Every story happened or was first reported on Friday 20 November 2026."
    ff = F(SERIF_B, 11.5)
    d.text(((W - tw(d, foot, ff)) / 2, fy + 4), foot, font=ff, fill=INK)
    srcs = ("Sources: Reuters - AP - AFP - BBC - Al Jazeera - UN News - IMD / The Hindu BusinessLine - ESA - ATP - "
            "Formula1.com - Sensor Tower via VGC - Dow Jones - People's Bank of China")
    sf2 = F(SANS, 8)
    d.text(((W - tw(d, srcs, sf2)) / 2, fy + 19), srcs, font=sf2, fill=SOFT)

    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img = build()
    assert img.size == (1024, 1024), img.size
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
