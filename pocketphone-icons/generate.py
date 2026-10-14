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

for name, glyph, pal in [("phone", handset(), GREEN), ("settings", gear(), GRAY)]:
    img = render(glyph, pal, name)
    img.save(f"{name}@16.png")
    img.resize((128, 128), Image.NEAREST).save(f"{name}.png")
    img.resize((512, 512), Image.NEAREST).save(f"{name}@512.png")
