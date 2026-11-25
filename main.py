import os
import struct
import zlib

W = 1024
H = 1024
BG = (13, 22, 36)
PANEL = (23, 40, 61)
PANEL2 = (18, 32, 50)
INK = (236, 241, 246)
MUTED = (148, 166, 184)
FAINT = (110, 128, 148)
RED = (226, 62, 52)
AMBER = (238, 178, 62)
TEAL = (74, 190, 178)
GREEN = (86, 198, 122)
BLUE = (96, 165, 250)
ORANGE = (244, 130, 48)
VIOLET = (178, 132, 245)
DOT = (88, 158, 178)
DOTDIM = (52, 96, 116)
GOODBG = (16, 52, 38)

FONT = {
"A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
"B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
"C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
"D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
"E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
"F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
"G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
"H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
"I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
"J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
"K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
"L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
"M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
"N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
"O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
"P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
"Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
"R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
"S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
"T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
"U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
"V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
"W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
"X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
"Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
"Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
"0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
"1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
"2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
"3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
"4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
"5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
"6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
"7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
"8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
"9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
"!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
"?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
"'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
'"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
"-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
"(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
"/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
"%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
"$": ("00100", "01110", "10100", "01110", "00101", "01110", "00100"),
"+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
"&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
"=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
"*": ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
" ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
}


def text_w(s, scale):
    return len(s) * (5 * scale + scale) - scale


def wrap(s, scale, maxw):
    words = s.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if cur == "" else cur + " " + word
        if text_w(trial, scale) <= maxw or cur == "":
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur != "":
        lines.append(cur)
    return lines


class Canvas:
    def __init__(self):
        self.buf = bytearray(bytes(BG) * (W * H))

    def set(self, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 3
            self.buf[i] = c[0]
            self.buf[i + 1] = c[1]
            self.buf[i + 2] = c[2]

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def hline(self, x, y, w, c):
        for xx in range(x, x + w):
            self.set(xx, y, c)

    def vline(self, x, y, h, c):
        for yy in range(y, y + h):
            self.set(x, yy, c)

    def disc(self, cx, cy, r, c):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            for xx in range(cx - dx, cx + dx + 1):
                self.set(xx, cy + dy, c)

    def ring(self, cx, cy, r, c):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.set(cx - dx, cy + dy, c)
            self.set(cx + dx, cy + dy, c)
            self.set(cx + dy, cy - dx, c)
            self.set(cx + dy, cy + dx, c)

    def glyph(self, ch, x, y, scale, c):
        g = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = g[row]
            for col in range(5):
                if bits[col] == "1":
                    for dy in range(scale):
                        for dx in range(scale):
                            self.set(x + col * scale + dx, y + row * scale + dy, c)

    def text(self, s, x, y, scale, c):
        cx = x
        for ch in s:
            self.glyph(ch, cx, y, scale, c)
            cx += 5 * scale + scale

    def center(self, s, y, scale, c, x0=0, x1=W):
        w = text_w(s, scale)
        self.text(s, x0 + (x1 - x0 - w) // 2, y, scale, c)

    def block(self, s, x, y, scale, maxw, c, leading=2, maxlines=99):
        lines = wrap(s, scale, maxw)
        n = min(len(lines), maxlines)
        for i in range(n):
            self.text(lines[i], x, y + i * (7 * scale + leading), scale, c)
        return y + n * (7 * scale + leading)


LAND = [
    [(12, 22), (25, 31), (38, 39)],
    [(3, 5), (10, 24), (25, 32), (45, 49), (54, 59), (63, 68)],
    [(2, 7), (8, 25), (26, 32), (38, 41), (44, 71)],
    [(2, 8), (9, 26), (33, 33), (37, 42), (43, 71)],
    [(2, 9), (9, 27), (34, 35), (37, 42), (43, 71)],
    [(3, 9), (10, 27), (34, 35), (37, 43), (44, 70)],
    [(10, 28), (34, 44), (45, 68), (69, 70)],
    [(11, 28), (34, 45), (46, 66), (68, 69)],
    [(11, 28), (34, 44), (45, 64), (65, 65), (67, 68)],
    [(11, 27), (34, 44), (45, 50), (55, 66), (67, 68)],
    [(13, 26), (33, 45), (46, 52), (53, 66)],
    [(13, 20), (24, 25), (33, 46), (47, 51), (54, 58), (60, 66)],
    [(14, 20), (33, 46), (47, 50), (55, 57), (60, 65)],
    [(15, 19), (33, 46), (55, 56), (61, 65)],
    [(16, 19), (34, 45), (60, 64)],
    [(20, 25), (34, 45), (60, 66)],
    [(20, 26), (34, 45), (61, 67)],
    [(20, 27), (35, 44), (62, 68)],
    [(20, 27), (35, 44), (62, 68)],
    [(21, 27), (35, 43), (60, 64), (63, 67)],
    [(21, 27), (35, 43), (45, 45), (59, 65)],
    [(21, 27), (35, 42), (45, 45), (58, 66)],
    [(21, 27), (35, 42), (58, 65), (69, 70)],
    [(22, 27), (36, 41), (59, 65), (69, 69)],
    [(22, 26), (60, 64), (69, 69)],
    [(22, 25), (69, 69)],
    [(22, 25)],
    [(22, 24)],
    [(22, 23)],
]

MAP_X0 = 80
MAP_Y0 = 100
MAP_DX = 12
MAP_DY = 9


def map_xy(lat, lon):
    x = MAP_X0 + (lon + 180.0) / 360.0 * 72 * MAP_DX
    y = MAP_Y0 + (82.5 - lat) / 5.0 * MAP_DY
    return int(x), int(y)


def draw_map(cv):
    for r, ranges in enumerate(LAND):
        cy = MAP_Y0 + r * MAP_DY
        for a, b in ranges:
            for col in range(a, b + 1):
                cx = MAP_X0 + col * MAP_DX + MAP_DX // 2
                c = DOT if (r + col) % 3 else DOTDIM
                cv.disc(cx, cy, 3, c)


def marker(cv, lat, lon, num, c):
    x, y = map_xy(lat, lon)
    cv.disc(x, y, 12, c)
    cv.ring(x, y, 12, INK)
    cv.text(str(num), x - 3, y - 4, 1, (10, 14, 20))


STORIES = [
    (1, "UKRAINE", RED, "OVERNIGHT STRIKE HITS FLATS IN ZAPORIZHZHIA",
     "2 KILLED, 40 WOUNDED, 4 OF THEM CHILDREN. RUSSIAN ATTACK HITS AN APARTMENT BLOCK OVERNIGHT.",
     47.85, 35.12),
    (2, "GAZA", ORANGE, "ISRAEL KILLS HAMAS SECURITY CHIEF",
     "NAEEM ABU NAHEL + 6 OTHERS DEAD IN AIRSTRIKES, 2 OF THEM POLICE, MEDICS SAY.",
     31.5, 34.45),
    (3, "IRAN", AMBER, "TRUMP SIGNALS NEW STRIKES ON IRAN",
     "NEW STRIKES IF TALKS FAIL. TEHRAN VOWS TO DEFY THE US NAVAL BLOCKADE. VANCE + RUBIO MET QATAR'S PM AT THE WHITE HOUSE.",
     35.7, 51.4),
    (4, "SPACE", BLUE, "NATO VOWS SPACE DEFENCE AS 'SPUTNIK-S' REPORTS SPREAD",
     "GERMAN MEDIA: RUSSIA READIES A NUCLEAR-ARMED SATELLITE, LAUNCH WITHIN 60 DAYS. KREMLIN: PROPAGANDA.",
     52.5, 13.4),
    (5, "BUSINESS", TEAL, "SANOFI BUYS INSMED FOR $41 BILLION",
     "BIGGEST BIOTECH DEAL IN ABOUT 3 YEARS. $175 A SHARE IN CASH. CLOSES IN THE FIRST HALF OF 2027.",
     48.85, 2.35),
    (6, "UN REPORT", VIOLET, "47,000 WOMEN KILLED BY PARTNERS",
     "UN: 47,000 KILLED IN 2025. FIVE EVERY HOUR, 129 A DAY. PARTNERS + FAMILY BEHIND 60% OF 78,000 FEMICIDES.",
     40.7, -74.0),
]

ALSO = [
    "NEPAL: 5.4 QUAKE HITS KOSHI PROVINCE; TREMORS FELT IN INDIA, BHUTAN, BANGLADESH AND CHINA. NO CASUALTIES REPORTED.",
    "DR CONGO: FIGHTING IN ITURI TRAPS EBOLA RESPONSE TEAMS NEAR A HOSPITAL FOR OVER 24 HOURS, WHO SAYS.",
    "GERMANY: FIRST COUNTRY GIVEN ACCESS TO UKRAINE'S DELTA BATTLEFIELD SYSTEM, KYIV SAYS.",
    "USA: STATES SUE MUSK'S FIRMS OVER SEXUALISED IMAGES FROM THE GROK CHATBOT.",
]


def draw_header(cv):
    cv.rect(0, 0, W, 6, RED)
    cv.center("THE WORLD IN ONE IMAGE", 18, 4, INK)
    cv.center("TUESDAY, 24 NOVEMBER 2026", 54, 2, MUTED)
    cv.hline(24, 76, W - 48, (52, 72, 96))
    cv.center("WHERE IT HAPPENED  -  SIX STORIES, ONE DAY", 86, 1, FAINT)


def draw_card(cv, x, y, story):
    num, tag, accent, head, facts, lat, lon = story
    cv.rect(x, y, 480, 118, PANEL)
    cv.rect(x, y, 6, 118, accent)
    cv.disc(x + 32, y + 26, 15, accent)
    cv.text(str(num), x + 29, y + 22, 1, (10, 14, 20))
    cv.text(tag, x + 54, y + 12, 1, accent)
    cv.text("MON 24 NOV", x + 480 - 14 - text_w("MON 24 NOV", 1), y + 12, 1, FAINT)
    lines = wrap(head, 2, 480 - 54 - 14)
    yy = y + 30
    for ln in lines[:2]:
        cv.text(ln, x + 54, yy, 2, INK)
        yy += 16
    cv.block(facts, x + 14, y + 70, 1, 480 - 28, MUTED, leading=2, maxlines=3)


def draw_also(cv):
    x, y = 24, 758
    cv.rect(x, y, 976, 104, PANEL2)
    cv.text("ALSO ON TUESDAY", x + 16, y + 12, 1, INK)
    for i, line in enumerate(ALSO):
        cv.text("-", x + 16, y + 34 + i * 16, 1, MUTED)
        cv.block(line, x + 30, y + 34 + i * 16, 1, 976 - 46, MUTED, leading=2, maxlines=1)


def draw_good(cv):
    x, y = 24, 876
    cv.rect(x, y, 976, 86, GOODBG)
    cv.rect(x, y, 6, 86, GREEN)
    cv.text("BRIGHTER NEWS", x + 20, y + 12, 2, GREEN)
    cv.text("+", x + 20, y + 40, 2, GREEN)
    cv.block("WALL STREET POSTS ITS BEST DAY IN OVER A YEAR AS NVIDIA SHARES RISE ON HUANG'S RETURN AS CEO.",
             x + 44, y + 42, 1, 440, INK, leading=2, maxlines=3)
    cv.text("+", x + 516, y + 40, 2, GREEN)
    cv.block("ASTRONOMERS FIND THE MOST DISTANT GLOWING BLACK HOLE YET: A QUASAR FROM WITHIN 630 MILLION YEARS OF THE BIG BANG.",
             x + 540, y + 42, 1, 440, INK, leading=2, maxlines=3)


def draw_footer(cv):
    cv.center("SOURCES: JUST SECURITY - REUTERS - BBC - UN NEWS - SANOFI - UN WOMEN - USGS", 978, 1, FAINT)
    cv.center("EVERY FACT AS REPORTED ON TUESDAY 24 NOVEMBER 2026", 990, 1, FAINT)


def build():
    cv = Canvas()
    draw_header(cv)
    draw_map(cv)
    for story in STORIES:
        marker(cv, story[5], story[6], story[0], story[2])
    for i, story in enumerate(STORIES):
        cx = 24 + (i % 2) * 496
        cy = 372 + (i // 2) * 128
        draw_card(cv, cx, cy, story)
    draw_also(cv)
    draw_good(cv)
    draw_footer(cv)
    return cv


def chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def png_bytes(cv):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += cv.buf[y * W * 3:(y + 1) * W * 3]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    out = bytearray(b"\x89PNG\r\n\x1a\n")
    out += chunk(b"IHDR", ihdr)
    out += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    out += chunk(b"IEND", b"")
    return bytes(out)


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    data = png_bytes(build())
    with open(os.path.join(outdir, "entry.png"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
