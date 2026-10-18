"""One cohesive Chicken Boom QR poster — reference-style."""

from __future__ import annotations

import math
import random
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from qrcode.constants import ERROR_CORRECT_H

URL = "https://chicken-boom-menu.vercel.app/"
ROOT = Path(__file__).resolve().parents[1]
OUT_QR = ROOT / "public" / "qr-menu.png"
OUT_POSTER = ROOT / "public" / "qr-poster.png"
LOGO = ROOT / "public" / "logo.png"
CHICKEN = ROOT / "public" / "chicken-cutout.jpg"

CREAM = (255, 248, 233)
FLAME = (224, 40, 43)
FLAME_DEEP = (176, 26, 29)
INK = (42, 10, 10)


def font(size: int, *, display: bool = False) -> ImageFont.ImageFont:
    paths = (
        [r"C:\Windows\Fonts\impact.ttf", r"C:\Windows\Fonts\arialbd.ttf"]
        if display
        else [r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\tahoma.ttf"]
    )
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def trim(img: Image.Image) -> Image.Image:
    bbox = img.getbbox()
    return img.crop(bbox) if bbox else img


def textured_red(w: int, h: int) -> Image.Image:
    rng = random.Random(11)
    img = Image.new("RGB", (w, h), FLAME)
    px = img.load()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            n = rng.randint(-20, 20)
            wave = int(10 * math.sin(x / 52) * math.cos(y / 68))
            r = max(150, min(238, FLAME[0] + n + wave - y // 90))
            g = max(20, min(60, FLAME[1] + n // 3))
            b = max(20, min(60, FLAME[2] + n // 3))
            c = (r, g, b)
            px[x, y] = c
            if x + 1 < w:
                px[x + 1, y] = c
            if y + 1 < h:
                px[x, y + 1] = c
                if x + 1 < w:
                    px[x + 1, y + 1] = c

    veil = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veil)
    for _ in range(12):
        y0 = rng.randint(0, h)
        vd.line(
            [(0, y0), (w, y0 + rng.randint(-120, 120))],
            fill=(255, 255, 255, rng.randint(8, 18)),
            width=rng.randint(55, 100),
        )
    veil = veil.filter(ImageFilter.GaussianBlur(28))
    return Image.alpha_composite(img.convert("RGBA"), veil)


def make_qr() -> Image.Image:
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=14, border=2)
    qr.add_data(URL)
    qr.make(fit=True)
    return qr.make_image(fill_color=FLAME, back_color=CREAM).convert("RGBA")


def rounded_card(qr: Image.Image, pad: int = 30, radius: int = 28) -> Image.Image:
    cw, ch = qr.size[0] + pad * 2, qr.size[1] + pad * 2
    base = Image.new("RGBA", (cw, ch), (*CREAM, 255))
    base.paste(qr, (pad, pad))
    mask = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw - 1, ch - 1), radius=radius, fill=255)
    out = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    out.paste(base, mask=mask)
    out.putalpha(mask)
    return out


def signal_arcs(draw: ImageDraw.ImageDraw, cx: int, cy: int, side: str) -> None:
    for i, rad in enumerate((24, 42, 60)):
        box = [cx - rad, cy - rad, cx + rad, cy + rad]
        width = 7 - i
        if side == "left":
            draw.arc(box, start=305, end=55, fill=CREAM, width=width)
        else:
            draw.arc(box, start=125, end=235, fill=CREAM, width=width)


def prepare_chicken(max_w: int) -> Image.Image:
    img = Image.open(CHICKEN).convert("RGBA")
    data = list(img.getdata())
    out = []
    for r, g, b, a in data:
        if r >= 236 and g >= 225 and b >= 195:
            out.append((r, g, b, 0))
        elif r >= 248 and g >= 248 and b >= 248:
            out.append((r, g, b, 0))
        else:
            out.append((r, g, b, a))
    img.putdata(out)
    img = trim(img)
    ratio = max_w / img.size[0]
    img = img.resize((max_w, max(1, int(img.size[1] * ratio))), Image.Resampling.LANCZOS)
    # gentle alpha soften
    a = img.getchannel("A").filter(ImageFilter.GaussianBlur(0.8))
    img.putalpha(a)
    return img


def build_poster(qr: Image.Image) -> Image.Image:
    W, H = 1080, 1620

    # base = cream (top + bottom match)
    poster = Image.new("RGBA", (W, H), (*CREAM, 255))

    # —— large logo on cream top ——
    logo = trim(Image.open(LOGO).convert("RGBA"))
    logo.thumbnail((340, 340), Image.Resampling.LANCZOS)
    logo_y = 28
    poster.paste(logo, ((W - logo.size[0]) // 2, logo_y), logo)
    logo_bottom = logo_y + logo.size[1]

    # —— red middle band (wavy top & bottom) ——
    red_top = logo_bottom + 18
    red_bottom = int(H * 0.74)
    red_band = textured_red(W, H)
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)

    # polygon: wavy top edge then wavy bottom edge
    pts: list[tuple[int, int]] = []
    for x in range(0, W + 1, 4):
        t = x / W
        y = red_top + int(28 * math.sin(math.pi * t))
        pts.append((x, y))
    for x in range(W, -1, -4):
        t = x / W
        y = red_bottom + int(70 * math.sin(math.pi * t)) - 10
        pts.append((x, y))
    md.polygon(pts, fill=255)
    poster = Image.composite(red_band, poster, mask)
    draw = ImageDraw.Draw(poster)

    # SCAN + pill + QR live in the red band
    scan_y = red_top + 36
    draw.text((W / 2, scan_y), "SCAN", fill=CREAM, font=font(132, display=True), anchor="mt")

    label = "to see our menu"
    pf = font(30)
    bb = draw.textbbox((0, 0), label, font=pf)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pw, ph = tw + 54, th + 24
    px0, py0 = (W - pw) // 2, scan_y + 122
    draw.rounded_rectangle((px0, py0, px0 + pw, py0 + ph), radius=ph // 2, fill=CREAM)
    draw.text((W / 2, py0 + ph / 2), label, fill=FLAME_DEEP, font=pf, anchor="mm")

    target = 340
    s = target / max(qr.size)
    qr_s = qr.resize((int(qr.size[0] * s), int(qr.size[1] * s)), Image.Resampling.LANCZOS)
    card = rounded_card(qr_s)
    cx = (W - card.size[0]) // 2
    cy = py0 + ph + 24

    shadow = Image.new("RGBA", (card.size[0] + 28, card.size[1] + 28), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (8, 10, card.size[0] + 8, card.size[1] + 12),
        radius=30,
        fill=(42, 10, 10, 55),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    poster.paste(shadow, (cx - 8, cy - 2), shadow)
    poster.paste(card, (cx, cy), card)

    mid = cy + card.size[1] // 2
    signal_arcs(draw, cx - 28, mid, "left")
    signal_arcs(draw, cx + card.size[0] + 28, mid, "right")

    # chicken on cream bottom, bridging into red a little
    if CHICKEN.exists():
        chick = prepare_chicken(int(W * 0.62))
        sw, sh = int(chick.size[0] * 0.78), 48
        contact = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        ImageDraw.Draw(contact).ellipse((0, 0, sw - 1, sh - 1), fill=(42, 10, 10, 45))
        contact = contact.filter(ImageFilter.GaussianBlur(12))

        hx = (W - chick.size[0]) // 2
        qr_bottom = cy + card.size[1] + 8
        crest = red_bottom + 40
        hy = crest - int(chick.size[1] * 0.55)
        if hy < qr_bottom:
            hy = qr_bottom
        poster.paste(contact, ((W - sw) // 2, hy + chick.size[1] - 36), contact)
        poster.paste(chick, (hx, hy), chick)

    return poster.convert("RGB")


def main() -> None:
    qr = make_qr()
    qr.save(OUT_QR, "PNG", optimize=True)
    print("qr", OUT_QR, qr.size)

    poster = build_poster(qr)
    poster.save(OUT_POSTER, "PNG", optimize=True)
    print("poster", OUT_POSTER, poster.size)


if __name__ == "__main__":
    main()
