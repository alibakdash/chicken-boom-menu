from pathlib import Path

import arabic_reshaper
import qrcode
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont
from qrcode.constants import ERROR_CORRECT_H


def arabic(text: str) -> str:
    return get_display(arabic_reshaper.reshape(text))

URL = "https://chicken-boom-menu.vercel.app/"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "qr-menu.png"
OUT_PRINT = ROOT / "public" / "qr-poster.png"
LOGO = ROOT / "public" / "logo.png"

CREAM = (255, 248, 233, 255)
FLAME = (224, 40, 43, 255)
YELLOW = (255, 184, 46, 255)
INK = (42, 10, 10, 255)
WHITE = (255, 255, 255, 255)


def load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def trim(img: Image.Image) -> Image.Image:
    bbox = img.getbbox()
    return img.crop(bbox) if bbox else img


def build_qr() -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=18,
        border=2,
    )
    qr.add_data(URL)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=(224, 40, 43), back_color=(255, 248, 233)).convert(
        "RGBA"
    )

    logo = trim(Image.open(LOGO).convert("RGBA"))
    logo_max = int(qr_img.size[0] * 0.26)
    logo.thumbnail((logo_max, logo_max), Image.Resampling.LANCZOS)

    pad = 18
    plate_size = max(logo.size) + pad * 2
    plate = Image.new("RGBA", (plate_size, plate_size), (0, 0, 0, 0))
    pd = ImageDraw.Draw(plate)
    pd.rounded_rectangle(
        (0, 0, plate_size - 1, plate_size - 1),
        radius=plate_size // 2,
        fill=WHITE,
    )
    pd.ellipse((3, 3, plate_size - 4, plate_size - 4), outline=YELLOW, width=6)
    plate.paste(logo, ((plate_size - logo.size[0]) // 2, (plate_size - logo.size[1]) // 2), logo)

    pos = ((qr_img.size[0] - plate_size) // 2, (qr_img.size[1] - plate_size) // 2)
    qr_img.paste(plate, pos, plate)
    return qr_img


def build_poster(qr_img: Image.Image) -> Image.Image:
    w, h = 1080, 1480
    poster = Image.new("RGBA", (w, h), CREAM)
    draw = ImageDraw.Draw(poster)

    draw.rectangle((0, 0, w, 220), fill=YELLOW)
    draw.rectangle((0, h - 160, w, h), fill=FLAME)
    draw.rectangle((0, 220, 18, h - 160), fill=FLAME)
    draw.rectangle((w - 18, 220, w, h - 160), fill=FLAME)

    header_logo = trim(Image.open(LOGO).convert("RGBA"))
    header_logo.thumbnail((170, 170), Image.Resampling.LANCZOS)
    poster.paste(header_logo, ((w - header_logo.size[0]) // 2, 28), header_logo)

    draw.text(
        (w // 2, 270),
        arabic("امسح لفتح المنيو"),
        fill=FLAME,
        font=load_font(54, True),
        anchor="mt",
    )
    draw.text((w // 2, 340), "Scan to open the menu", fill=INK, font=load_font(28), anchor="mt")

    card_pad = 40
    scale = min(720 / qr_img.size[0], 720 / qr_img.size[1])
    qr_big = qr_img.resize(
        (int(qr_img.size[0] * scale), int(qr_img.size[1] * scale)),
        Image.Resampling.LANCZOS,
    )
    cw, ch = qr_big.size[0] + card_pad * 2, qr_big.size[1] + card_pad * 2
    card = Image.new("RGBA", (cw, ch), WHITE)
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((0, 0, cw - 1, ch - 1), radius=36, fill=WHITE, outline=YELLOW, width=8)
    card.paste(qr_big, (card_pad, card_pad), qr_big)

    cx = (w - cw) // 2
    cy = 400
    shadow = Image.new("RGBA", (cw + 20, ch + 20), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((10, 10, cw + 10, ch + 10), radius=36, fill=(42, 10, 10, 40))
    poster.paste(shadow, (cx - 10, cy - 4), shadow)
    poster.paste(card, (cx, cy), card)

    draw.text(
        (w // 2, h - 100),
        "chicken-boom-menu.vercel.app",
        fill=WHITE,
        font=load_font(30, True),
        anchor="mt",
    )
    draw.text((w // 2, h - 55), "CHICKEN BOOM", fill=YELLOW, font=load_font(26, True), anchor="mt")
    return poster.convert("RGB")


def main() -> None:
    qr_img = build_qr()
    qr_img.save(OUT, "PNG", optimize=True)
    print(f"saved {OUT} {qr_img.size}")

    poster = build_poster(qr_img)
    poster.save(OUT_PRINT, "PNG", optimize=True)
    print(f"saved {OUT_PRINT} {poster.size}")


if __name__ == "__main__":
    main()
