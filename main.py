# News Image 24 Nov 2026 — draws Tuesday's world news as one 1024x1024 PNG.
# Pure stdlib: os, struct, zlib. No network, no files read, no fonts on disk.
# Every glyph is one 35-character string (7 rows of 5 bits, top to bottom).
# Run: python3 main.py  ->  writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output).

import os
import struct
import zlib

W, H = 1024, 1024
BG, PANEL, PANEL2 = (13, 22, 36), (23, 40, 61), (18, 32, 50)
INK, MUTED, FAINT = (236, 241, 246), (148, 166, 184), (110, 128, 148)
RED, AMBER, TEAL = (226, 62, 52), (238, 178, 62), (74, 190, 178)
GREEN, BLUE, ORANGE = (86, 198, 122), (96, 165, 250), (244, 130, 48)
VIOLET, DOT, DOTDIM = (178, 132, 245), (88, 158, 178), (52, 96, 116)
GOODBG, DARK, RULE = (16, 52, 38), (10, 14, 20), (52, 72, 96)
BLANK = "00000000000000000000000000000000000"

GLYPHS = {
    "A": "01110100011000111111100011000110001",
    "B": "11110100011000111110100011000111110",
    "C": "01110100011000010000100001000101110",
    "D": "11110100011000110001100011000111110",
    "E": "11111100001000011110100001000011111",
    "F": "11111100001000011110100001000010000",
    "G": "01110100011000010111100011000101111",
    "H": "10001100011000111111100011000110001",
    "I": "01110001000010000100001000010001110",
    "J": "00111000100001000010000101001001100",
    "K": "10001100101010011000101001001010001",
    "L": "10000100001000010000100001000011111",
    "M": "10001110111010110101100011000110001",
    "N": "10001110011010110011100011000110001",
    "O": "01110100011000110001100011000101110",
    "P": "11110100011000111110100001000010000",
    "Q": "01110100011000110001101011001001101",
    "R": "11110100011000111110101001001010001",
    "S": "01111100001000001110000010000111110",
    "T": "11111001000010000100001000010000100",
    "U": "10001100011000110001100011000101110",
    "V": "10001100011000110001100010101000100",
    "W": "10001100011000110101101011101110001",
    "X": "10001100010101000100010101000110001",
    "Y": "10001100010101000100001000010000100",
    "Z": "11111000010001000100010001000011111",
    "0": "01110100011001110101110011000101110",
    "1": "00100011000010000100001000010001110",
    "2": "01110100010000100110010001000011111",
    "3": "11111000100010000010000011000101110",
    "4": "00010001100101010010111110001000010",
    "5": "11111100001111000001000011000101110",
    "6": "00110010001000011110100011000101110",
    "7": "11111000010001000100010000100001000",
    "8": "01110100011000101110100011000101110",
    "9": "01110100011000101111000010001001100",
    ".": "00000000000000000000000000110001100",
    ",": "00000000000000000000011000010001000",
    ":": "00000011000110000000011000110000000",
    ";": "00000011000110000000011000010001000",
    "!": "00100001000010000100001000000000100",
    "?": "01110100010000100110001000000000100",
    "'": "00100001000100000000000000000000000",
    '"': "01010010100000000000000000000000000",
    "-": "00000000000000001110000000000000000",
    "(": "00010001000100001000010000010000010",
    ")": "01000001000001000010000100010001000",
    "/": "00001000100001000100010000100010000",
    "%": "11001110100001000100010000101110011",
    "+": "00000001000010001110001000010000000",
    "&": "01100100101010001000101011001001101",
    "=": "00000000001111100000111110000000000",
    "*": "00000101010111010101000000000000000",
    "$": "00100011101010001110001010111000100",
    " ": BLANK,
}


def glyph_bits(ch):
    return GLYPHS.get(ch, BLANK)


def text_width(s, scale):
    return len(s) * 6 * scale - scale


def wrap_lines(s, scale, maxw):
    lines, cur = [], ""
    for word in s.split(" "):
        trial = word if cur == "" else cur + " " + word
        if text_width(trial, scale) <= maxw or cur == "":
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

    def put(self, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 3
            self.buf[i:i + 3] = bytes(c)

    def fill(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.put(xx, yy, c)

    def hline(self, x, y, w, c):
        for xx in range(x, x + w):
            self.put(xx, y, c)

    def vline(self, x, y, h, c):
        for yy in range(y, y + h):
            self.put(x, yy, c)

    def disc(self, cx, cy, r, c):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            for xx in range(cx - dx, cx + dx + 1):
                self.put(xx, cy + dy, c)

    def ring(self, cx, cy, r, c):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.put(cx - dx, cy + dy, c)
            self.put(cx + dx, cy + dy, c)
            self.put(cx + dy, cy - dx, c)
            self.put(cx + dy, cy + dx, c)

    def glyph(self, ch, x, y, scale, c):
        bits = glyph_bits(ch)
        for row in range(7):
            for col in range(5):
                if bits[row * 5 + col] == "1":
                    for dy in range(scale):
                        for dx in range(scale):
                            self.put(x + col * scale + dx, y + row * scale + dy, c)

    def text(self, s, x, y, scale, c):
        cx = x
        for ch in s:
            self.glyph(ch, cx, y, scale, c)
            cx += 6 * scale

    def center(self, s, y, scale, c, x0=0, x1=W):
        w = text_width(s, scale)
        self.text(s, x0 + (x1 - x0 - w) // 2, y, scale, c)

    def block(self, s, x, y, scale, maxw, c, leading=2, maxlines=99):
        lines = wrap_lines(s, scale, maxw)
        n = min(len(lines), maxlines)
        for i in range(n):
            self.text(lines[i], x, y + i * (7 * scale + leading), scale, c)
        return y + n * (7 * scale + leading)


# World map: 29 rows, 72 columns. Each row lists the land runs as "a-b,c-d".
LAND = [
    "12-22,25-31,38-39",
    "3-5,10-24,25-32,45-49,54-59,63-68",
    "2-7,8-25,26-32,38-41,44-71",
    "2-8,9-26,33-33,37-42,43-71",
    "2-9,9-27,34-35,37-42,43-71",
    "3-9,10-27,34-35,37-43,44-70",
    "10-28,34-44,45-68,69-70",
    "11-28,34-45,46-66,68-69",
    "11-28,34-44,45-64,65-65,67-68",
    "11-27,34-44,45-50,55-66,67-68",
    "13-26,33-45,46-52,53-66",
    "13-20,24-25,33-46,47-51,54-58,60-66",
    "14-20,33-46,47-50,55-57,60-65",
    "15-19,33-46,55-56,61-65",
    "16-19,34-45,60-64",
    "20-25,34-45,60-66",
    "20-26,34-45,61-67",
    "20-27,35-44,62-68",
    "20-27,35-44,62-68",
    "21-27,35-43,60-64,63-67",
    "21-27,35-43,45-45,59-65",
    "21-27,35-42,45-45,58-66",
    "21-27,35-42,58-65,69-70",
    "22-27,36-41,59-65,69-69",
    "22-26,60-64,69-69",
    "22-25,69-69",
    "22-25",
    "22-24",
    "22-23",
]
MAP_X, MAP_Y, MAP_DX, MAP_DY = 80, 100, 12, 9


def geo_to_xy(lat, lon):
    px = MAP_X + (lon + 180.0) / 360.0 * 72 * MAP_DX
    py = MAP_Y + (82.5 - lat) / 5.0 * MAP_DY
    return int(px), int(py)


def land_cols(row):
    out = []
    for part in LAND[row].split(","):
        a, b = part.split("-")
        out.extend(range(int(a), int(b) + 1))
    return out


def draw_map(cv):
    for r in range(len(LAND)):
        cy = MAP_Y + r * MAP_DY
        for col in land_cols(r):
            cx = MAP_X + col * MAP_DX + MAP_DX // 2
            shade = DOT if (r + col) % 3 else DOTDIM
            cv.disc(cx, cy, 3, shade)


def marker(cv, lat, lon, num, c):
    x, y = geo_to_xy(lat, lon)
    cv.disc(x, y, 12, c)
    cv.ring(x, y, 12, INK)
    cv.text(str(num), x - 3, y - 4, 1, DARK)


STORIES = [
    {"num": 1, "tag": "UKRAINE", "hue": RED,
     "head": "OVERNIGHT STRIKE HITS FLATS IN ZAPORIZHZHIA",
     "body": "2 KILLED, 40 WOUNDED, 4 OF THEM CHILDREN. RUSSIAN ATTACK HITS AN APARTMENT BLOCK OVERNIGHT.",
     "lat": 47.85, "lon": 35.12},
    {"num": 2, "tag": "GAZA", "hue": ORANGE,
     "head": "ISRAEL KILLS HAMAS SECURITY CHIEF",
     "body": "NAEEM ABU NAHEL + 6 OTHERS DEAD IN AIRSTRIKES, 2 OF THEM POLICE, MEDICS SAY.",
     "lat": 31.5, "lon": 34.45},
    {"num": 3, "tag": "IRAN", "hue": AMBER,
     "head": "TRUMP SIGNALS NEW STRIKES ON IRAN",
     "body": "NEW STRIKES IF TALKS FAIL. TEHRAN VOWS TO DEFY THE US NAVAL BLOCKADE. VANCE + RUBIO MET QATAR'S PM AT THE WHITE HOUSE.",
     "lat": 35.7, "lon": 51.4},
    {"num": 4, "tag": "SPACE", "hue": BLUE,
     "head": "NATO VOWS SPACE DEFENCE AS 'SPUTNIK-S' REPORTS SPREAD",
     "body": "GERMAN MEDIA: RUSSIA READIES A NUCLEAR-ARMED SATELLITE, LAUNCH WITHIN 60 DAYS. KREMLIN: PROPAGANDA.",
     "lat": 52.5, "lon": 13.4},
    {"num": 5, "tag": "BUSINESS", "hue": TEAL,
     "head": "SANOFI BUYS INSMED FOR $41 BILLION",
     "body": "BIGGEST BIOTECH DEAL IN ABOUT 3 YEARS. $175 A SHARE IN CASH. CLOSES IN THE FIRST HALF OF 2027.",
     "lat": 48.85, "lon": 2.35},
    {"num": 6, "tag": "UN REPORT", "hue": VIOLET,
     "head": "47,000 WOMEN KILLED BY PARTNERS",
     "body": "UN: 47,000 KILLED IN 2025. FIVE EVERY HOUR, 129 A DAY. PARTNERS + FAMILY BEHIND 60% OF 78,000 FEMICIDES.",
     "lat": 40.7, "lon": -74.0},
]

ALSO = ("NEPAL: 5.4 QUAKE HITS KOSHI PROVINCE; TREMORS FELT IN INDIA, BHUTAN, BANGLADESH AND CHINA. NO CASUALTIES REPORTED."
        " | DR CONGO: FIGHTING IN ITURI TRAPS EBOLA RESPONSE TEAMS NEAR A HOSPITAL FOR OVER 24 HOURS, WHO SAYS."
        " | GERMANY: FIRST COUNTRY GIVEN ACCESS TO UKRAINE'S DELTA BATTLEFIELD SYSTEM, KYIV SAYS."
        " | USA: STATES SUE MUSK'S FIRMS OVER SEXUALISED IMAGES FROM THE GROK CHATBOT.")

GOOD_LEFT = "WALL STREET POSTS ITS BEST DAY IN OVER A YEAR AS NVIDIA SHARES RISE ON HUANG'S RETURN AS CEO."
GOOD_RIGHT = "ASTRONOMERS FIND THE MOST DISTANT GLOWING BLACK HOLE YET: A QUASAR FROM WITHIN 630 MILLION YEARS OF THE BIG BANG."


def draw_header(cv):
    cv.fill(0, 0, W, 6, RED)
    cv.center("THE WORLD IN ONE IMAGE", 18, 4, INK)
    cv.center("TUESDAY, 24 NOVEMBER 2026", 54, 2, MUTED)
    cv.hline(24, 76, W - 48, RULE)
    cv.center("WHERE IT HAPPENED  -  SIX STORIES, ONE DAY", 86, 1, FAINT)


def draw_card(cv, x, y, s):
    cv.fill(x, y, 480, 118, PANEL)
    cv.fill(x, y, 6, 118, s["hue"])
    cv.disc(x + 32, y + 26, 15, s["hue"])
    cv.text(str(s["num"]), x + 29, y + 22, 1, DARK)
    cv.text(s["tag"], x + 54, y + 12, 1, s["hue"])
    cv.text("MON 24 NOV", x + 480 - 14 - text_width("MON 24 NOV", 1), y + 12, 1, FAINT)
    heads = wrap_lines(s["head"], 2, 480 - 54 - 14)
    yy = y + 30
    for ln in heads[:2]:
        cv.text(ln, x + 54, yy, 2, INK)
        yy += 16
    cv.block(s["body"], x + 14, y + 70, 1, 480 - 28, MUTED, leading=2, maxlines=3)


def draw_also(cv):
    x, y = 24, 758
    cv.fill(x, y, 976, 104, PANEL2)
    cv.text("ALSO ON TUESDAY", x + 16, y + 12, 1, INK)
    for i, line in enumerate(ALSO.split(" | ")):
        cv.text("-", x + 16, y + 34 + i * 16, 1, MUTED)
        cv.block(line, x + 30, y + 34 + i * 16, 1, 976 - 46, MUTED, leading=2, maxlines=1)


def draw_good(cv):
    x, y = 24, 876
    cv.fill(x, y, 976, 86, GOODBG)
    cv.fill(x, y, 6, 86, GREEN)
    cv.text("BRIGHTER NEWS", x + 20, y + 12, 2, GREEN)
    cv.text("+", x + 20, y + 40, 2, GREEN)
    cv.block(GOOD_LEFT, x + 44, y + 42, 1, 440, INK, leading=2, maxlines=3)
    cv.text("+", x + 516, y + 40, 2, GREEN)
    cv.block(GOOD_RIGHT, x + 540, y + 42, 1, 440, INK, leading=2, maxlines=3)


def draw_footer(cv):
    cv.center("SOURCES: JUST SECURITY - REUTERS - BBC - UN NEWS - SANOFI - UN WOMEN - USGS", 978, 1, FAINT)
    cv.center("EVERY FACT AS REPORTED ON TUESDAY 24 NOVEMBER 2026", 990, 1, FAINT)


def build():
    cv = Canvas()
    draw_header(cv)
    draw_map(cv)
    for s in STORIES:
        marker(cv, s["lat"], s["lon"], s["num"], s["hue"])
    for i, s in enumerate(STORIES):
        draw_card(cv, 24 + (i % 2) * 496, 372 + (i // 2) * 128, s)
    draw_also(cv)
    draw_good(cv)
    draw_footer(cv)
    return cv


def png_chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def png_bytes(cv):
    raw = b"".join(b"\x00" + bytes(cv.buf[y * W * 3:(y + 1) * W * 3]) for y in range(H))
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", ihdr)
            + png_chunk(b"IDAT", zlib.compress(raw, 9))
            + png_chunk(b"IEND", b""))


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    data = png_bytes(build())
    with open(os.path.join(outdir, "entry.png"), "wb") as f:
        f.write(data)
    print("wrote", os.path.join(outdir, "entry.png"), len(data), "bytes")


if __name__ == "__main__":
    main()
