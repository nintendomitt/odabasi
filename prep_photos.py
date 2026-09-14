# -*- coding: utf-8 -*-
"""Stok fotograflari indirir, kirpar ve site icin optimize eder.

Kaynak: Unsplash (Unsplash License - ticari kullanim serbest, atif zorunlu degil)
Cikti:  assets_src/foto/<slug>.webp

Kullanim: python3 prep_photos.py [--force]
"""
import os, sys, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "photos_raw")
OUT = os.path.join(HERE, "assets_src", "foto")

# slug -> (unsplash photo id, hedef en, hedef boy)
CARD = (900, 600)      # kategori kartlari 3:2
WIDE = (1600, 900)     # hero / genis bantlar 16:9

PHOTOS = {
    # hero ve genel
    "hero":            ("1484154218962-a197022b5858", WIDE),
    "magaza":          ("1783700776216-cf661c778151", WIDE),
    # kategoriler
    "buzdolabi":            ("1588854337115-1c67d9247e4d", CARD),
    "camasir-makinesi":     ("1626806787461-102c1bfaaea1", CARD),
    "bulasik-makinesi":     ("1581622558663-b2e33377dfb2", CARD),
    "kurutma-makinesi":     ("1655041448985-f6666cba2d6c", CARD),
    "ankastre-set":         ("1772567732993-3c546ee1a52c", CARD),
    "klima":                ("1721045030396-a6af775ba1f7", CARD),
    "derin-dondurucu":      ("1601599967100-f16100982063", CARD),
    "ticari-sogutma":       ("1601599561096-f87c95fff1e9", CARD),
    "televizyon":           ("1761330439671-a7f20c285c5e", CARD),
    "kucuk-ev-aletleri":    ("1654064754916-e3edeb09c042", CARD),
    "temizlik-ekipmanlari": ("1765970101654-337b573142fb", CARD),
}

SRC = "https://images.unsplash.com/photo-%s?auto=format&fit=crop&w=2000&q=80"


def fetch(slug, pid):
    dst = os.path.join(RAW, "src_%s.jpg" % slug)
    if os.path.exists(dst) and os.path.getsize(dst) > 20000:
        return dst
    os.makedirs(RAW, exist_ok=True)
    subprocess.run(["curl", "-sS", "-m", "60", "-o", dst, SRC % pid], check=True)
    return dst


def cover(im, w, h):
    """Oranı bozmadan hedef kutuyu doldurur, ortadan kirpar."""
    s = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))


def main():
    os.makedirs(OUT, exist_ok=True)
    force = "--force" in sys.argv
    for slug, (pid, size) in PHOTOS.items():
        dst = os.path.join(OUT, slug + ".webp")
        if os.path.exists(dst) and not force:
            print("%-22s atlandi" % slug); continue
        src = fetch(slug, pid)
        im = Image.open(src).convert("RGB")
        cover(im, *size).save(dst, "WEBP", quality=74, method=6)
        print("%-22s %dx%d  %5.1f KB" % (slug, size[0], size[1], os.path.getsize(dst) / 1024))


if __name__ == "__main__":
    main()
