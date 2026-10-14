"""Genereert de pocketphone-iconen in Minecraft-stijl (16x16 pixels, opgeschaald)."""
import random
from PIL import Image

N = 16


def handset():
    # Bovenste helft (oorstuk + begin handvat); de rest is gespiegeld in de anti-diagonaal.
    half = {2: (3, 5), 3: (2, 6), 4: (2, 6), 5: (2, 5), 6: (2, 5), 7: (3, 5), 8: (4, 6), 9: (5, 7)}
    pts = {(x, y) for y, (a, b) in half.items() for x in range(a, b + 1)}
    return pts | {(15 - y, 15 - x) for x, y in pts}


def gear():
    pts = set()
    body = {4: (5, 10), 11: (5, 10)}
    for y in range(4, 12):
        a, b = body.get(y, (4, 11))
        pts |= {(x, y) for x in range(a, b + 1)}
    for a in range(6, 10):
        pts |= {(a, 2), (a, 3), (a, 12), (a, 13), (2, a), (3, a), (12, a), (13, a)}
    for cx, cy in [(3, 3), (11, 3), (3, 11), (11, 11)]:
        pts |= {(cx + dx, cy + dy) for dx in (0, 1) for dy in (0, 1)}
    hole = {(x, y) for x in range(6, 10) for y in range(6, 10)} - {(6, 6), (9, 6), (6, 9), (9, 9)}
    return pts - hole


def rows(spec):
    """{rij: [(van, tot), ...]} -> set van (x, y)."""
    return {(x, y) for y, spans in spec.items() for a, b in spans for x in range(a, b + 1)}


def bubble():
    return rows({3: [(4, 11)], 4: [(3, 12)], 5: [(2, 13)], 6: [(2, 13)], 7: [(2, 13)], 8: [(2, 13)],
                 9: [(3, 12)], 10: [(3, 11)], 11: [(3, 5)], 12: [(2, 3)]})


def camera():
    body = rows({3: [(3, 6)], 4: [(2, 13)], 5: [(2, 13)], 6: [(2, 13)], 7: [(2, 13)], 8: [(2, 13)],
                 9: [(2, 13)], 10: [(2, 13)], 11: [(2, 13)], 12: [(3, 12)]})
    lens = rows({6: [(6, 9)], 7: [(5, 10)], 8: [(5, 10)], 9: [(5, 10)], 10: [(5, 10)], 11: [(6, 9)]})
    core = rows({8: [(7, 8)], 9: [(7, 8)]})
    flash = {(11, 5), (12, 5)}
    return (body - lens - flash) | core


def picture():
    card = rows({y: [(2, 13)] for y in range(3, 13)})
    sun = rows({5: [(9, 10)], 6: [(9, 10)]})
    hills = rows({7: [(5, 5)], 8: [(4, 6)], 9: [(3, 7), (10, 10)], 10: [(3, 12)], 11: [(3, 12)]})
    return card - sun - hills


def render(glyph, pal, seed):
    rnd = random.Random(seed)
    img = Image.new("RGBA", (N, N))
    for y in range(N):
        for x in range(N):
            c = rnd.choice([pal["base"]] * 3 + [pal["dark"], pal["light"]])
            if x == 0 or y == 0:
                c = pal["edge_hi"]
            if x == N - 1 or y == N - 1:
                c = pal["edge_lo"]
            if (x, y - 1) in glyph and (x, y) not in glyph:
                c = pal["shadow"]
            if (x, y) in glyph:
                if (x, y + 1) not in glyph:
                    c = (208, 208, 214)
                else:
                    c = (255, 255, 255)
            img.putpixel((x, y), (*c, 255))
    return img


GREEN = dict(base=(52, 199, 89), dark=(46, 186, 82), light=(60, 210, 98),
             edge_hi=(98, 222, 128), edge_lo=(38, 160, 70), shadow=(28, 128, 56))
GRAY = dict(base=(142, 142, 147), dark=(133, 133, 138), light=(152, 152, 157),
            edge_hi=(175, 175, 180), edge_lo=(112, 112, 117), shadow=(92, 92, 97))



def palette(r, g, b):
    def mul(f):
        return tuple(max(0, min(255, round(v * f))) for v in (r, g, b))

    hi = tuple(round(v + (255 - v) * 0.3) for v in (r, g, b))
    return dict(base=(r, g, b), dark=mul(0.94), light=mul(1.06), edge_hi=hi, edge_lo=mul(0.8), shadow=mul(0.64))


BLUE = palette(10, 132, 255)
CHARCOAL = palette(72, 72, 78)
ORANGE = palette(255, 149, 0)

ICONS = [("phone", handset(), GREEN), ("settings", gear(), GRAY), ("messages", bubble(), BLUE),
         ("camera", camera(), CHARCOAL), ("gallery", picture(), ORANGE)]

for name, glyph, pal in ICONS:
    img = render(glyph, pal, name)
    img.save(f"{name}@16.png")
    img.resize((128, 128), Image.NEAREST).save(f"{name}.png")
    img.resize((512, 512), Image.NEAREST).save(f"{name}@512.png")
