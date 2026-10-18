from pathlib import Path
import math
import random

import qrcode
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from qrcode.constants import ERROR_CORRECT_H

URL = "https://chicken-boom-menu.vercel.app/"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "qr-menu.png"
OUT_PRINT = ROOT / "public" / "qr-poster.png"
HERO = ROOT / "public" / "qr-chicken-hero.jpg"

CREAM = (255, 248, 233)
CREAM_SOFT = (255, 250, 240)
FLAME = (224, 40, 43)
FLAME_DEEP = (185, 28, 31)
INK = (42, 10, 10)


def load_font(size: int, bold: bool = False, display: bool = False) -> ImageFont.ImageFont:
    if display:
        candidates = [
            r"C:\Windows\Fonts\impact.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf",
        ]
    else:
        candidates = [
            r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\tahoma.ttf",
        ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def textured_red(size: tuple[int, int]) -> Image.Image:
    w, h = size
    base = Image.new("RGB", size, FLAME)
    px = base.load()
    rng = random.Random(42)
    for y in range(h):
        for x in range(w):
            n = rng.randint(-28, 28)
            wave = int(14 * math.sin(x / 55.0) * math.cos(y / 70.0))
            r = max(150, min(245, FLAME[0] + n + wave))
            g = max(20, min(70, FLAME[1] + n // 2))
            b = max(20, min(70, FLAME[2] + n // 2))
            # deeper top vignette
            shade = int((y / h) * 18)
            px[x, y] = (max(130, r - shade), max(15, g - shade // 2), max(15, b - shade // 2))
    # soft marble streaks
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(18):
        y0 = rng.randint(0, h)
        od.line(
            [(0, y0), (w, y0 + rng.randint(-120, 120))],
            fill=(255, 255, 255, rng.randint(8, 22)),
            width=rng.randint(40, 90),
        )
    overlay = overlay.filter(ImageFilter.GaussianBlur(28))
    return Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")


def build_qr(with_logo: bool = False) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=16,
        border=2,
    )
    qr.add_data(URL)
    qr.make(fit=True)
    return qr.make_image(fill_color=FLAME, back_color=CREAM).convert("RGBA")


def draw_signal(draw: ImageDraw.ImageDraw, cx: int, cy: int, facing: str) -> None:
    """WiFi-like arcs pointing toward the QR."""
    for i, radius in enumerate((28, 48, 68)):
        width = 7 - i
        bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
        if facing == "right":
            # arcs open to the right (on left side of QR)
            draw.arc(bbox, start=300, end=60, fill=CREAM, width=width)
        else:
            draw.arc(bbox, start=120, end=240, fill=CREAM, width=width)


def rounded_rect_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def build_poster(qr_img: Image.Image) -> Image.Image:
    w, h = 1080, 1620
    poster = textured_red((w, h)).convert("RGBA")
    draw = ImageDraw.Draw(poster)

    # cream wave bottom
    wave = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wave)
    wave_y = int(h * 0.72)
    points = [(0, h), (0, wave_y)]
    for x in range(0, w + 1, 8):
        y = wave_y + int(48 * math.sin((x / w) * math.pi))
        points.append((x, y))
    points.append((w, h))
    wd.polygon(points, fill=CREAM + (255,))
    poster = Image.alpha_composite(poster, wave)
    draw = ImageDraw.Draw(poster)

    # brand / handle row
    draw.text((w // 2, 70), "CHICKEN BOOM", fill=CREAM, font=load_font(28, True), anchor="mt")

    # SCAN
    draw.text((w // 2, 190), "SCAN", fill=CREAM, font=load_font(168, True, display=True), anchor="mt")

    # pill CTA
    pill_text = "to see our menu"
    pill_font = load_font(36, True)
    tb = draw.textbbox((0, 0), pill_text, font=pill_font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    pill_w, pill_h = tw + 70, th + 34
    pill_x = (w - pill_w) // 2
    pill_y = 360
    draw.rounded_rectangle(
        (pill_x, pill_y, pill_x + pill_w, pill_y + pill_h),
        radius=pill_h // 2,
        fill=CREAM,
    )
    draw.text(
        (w // 2, pill_y + pill_h // 2),
        pill_text,
        fill=FLAME_DEEP,
        font=pill_font,
        anchor="mm",
    )

    # QR card
    card_pad = 36
    target = 460
    scale = target / max(qr_img.size)
    qr_big = qr_img.resize(
        (int(qr_img.size[0] * scale), int(qr_img.size[1] * scale)),
        Image.Resampling.LANCZOS,
    )
    cw = qr_big.size[0] + card_pad * 2
    ch = qr_big.size[1] + card_pad * 2
    card = Image.new("RGBA", (cw, ch), CREAM + (255,))
    mask = rounded_rect_mask((cw, ch), 28)
    card_draw = ImageDraw.Draw(card)
    card_draw.rounded_rectangle((0, 0, cw - 1, ch - 1), radius=28, fill=CREAM, outline=CREAM)
    card.paste(qr_big, (card_pad, card_pad))
    card.putalpha(mask)

    cx = (w - cw) // 2
    cy = 470
    # soft shadow under card
    shadow = Image.new("RGBA", (cw + 24, ch + 24), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (8, 10, cw + 8, ch + 12),
        radius=30,
        fill=(42, 10, 10, 55),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    poster.paste(shadow, (cx - 8, cy - 4), shadow)
    poster.paste(card, (cx, cy), card)

    # signal arcs
    mid_y = cy + ch // 2
    draw_signal(draw, cx - 36, mid_y, "right")
    draw_signal(draw, cx + cw + 36, mid_y, "left")

    # crispy chicken hero on the wave (like the steak in the reference)
    if HERO.exists():
        from PIL import ImageChops

        hero = Image.open(HERO).convert("RGBA")
        # focus crop on the chicken stack
        bw, bh = hero.size
        hero = hero.crop((int(bw * 0.08), int(bh * 0.02), int(bw * 0.92), int(bh * 0.92)))

        hero_w = int(w * 0.98)
        ratio = hero_w / hero.size[0]
        hero = hero.resize((hero_w, int(hero.size[1] * ratio)), Image.Resampling.LANCZOS)

        # soft oval mask so chicken sits naturally on the cream wave
        mask = Image.new("L", hero.size, 0)
        md = ImageDraw.Draw(mask)
        md.ellipse(
            (-int(hero.size[0] * 0.05), int(hero.size[1] * 0.05), int(hero.size[0] * 1.05), int(hero.size[1] * 1.15)),
            fill=255,
        )
        mask = mask.filter(ImageFilter.GaussianBlur(18))
        r, g, b, a = hero.split()
        hero = Image.merge("RGBA", (r, g, b, ImageChops.multiply(a, mask)))

        hx = (w - hero.size[0]) // 2
        hy = int(h * 0.70)
        poster.paste(hero, (hx, hy), hero)

    return poster.convert("RGB")


def main() -> None:
    qr_img = build_qr()
    # clean QR for sharing / print embeds
    qr_img.save(OUT, "PNG", optimize=True)
    print(f"saved {OUT} {qr_img.size}")

    poster = build_poster(qr_img)
    poster.save(OUT_PRINT, "PNG", optimize=True)
    print(f"saved {OUT_PRINT} {poster.size}")


if __name__ == "__main__":
    main()
