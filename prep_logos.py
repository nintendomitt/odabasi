# -*- coding: utf-8 -*-
"""Marka logolarini siteye uygun hale getirir.

- Disaridan iceri dogru tasan beyaz/acik zemini seffaf yapar
  (logonun ICINDEKI beyaz alanlar korunur - orn. LG dairesindeki beyaz yaylar)
- Bos kenarlari kirpar
- Sabit yukseklige olceklendirir, PNG olarak assets_src/markalar/ altina yazar

Kullanim:  python3 prep_logos.py <slug>=<dosya> [<slug>=<dosya> ...]
"""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets_src", "markalar")
BOX_W, BOX_H = 640, 200   # tum logolar bu kutuya yerlesir (2x pay birakildi)
TARGET_INK = 34000        # hedef murekkep alani (px^2) - optik agirlik esitlemesi
WHITE_TOL = 18          # bu esigin uzerindeki kanallar "beyaz" sayilir (255 - tol)


def strip_background(im):
    """Kenarlardan baglantili beyaz alani seffaf yapar."""
    im = im.convert("RGBA")
    a = np.array(im)
    rgb, alpha = a[..., :3].astype(int), a[..., 3]

    near_white = (rgb.min(axis=2) >= 255 - WHITE_TOL) & (alpha > 0)
    transparent = alpha == 0
    bg_candidate = near_white | transparent

    lab, n = ndimage.label(bg_candidate)
    if n == 0:
        return im
    # kenara degen bilesenler = arka plan
    edge = set(lab[0, :].tolist()) | set(lab[-1, :].tolist()) | \
           set(lab[:, 0].tolist()) | set(lab[:, -1].tolist())
    edge.discard(0)
    if not edge:
        return im
    mask = np.isin(lab, list(edge))
    a[..., 3] = np.where(mask, 0, alpha)
    return Image.fromarray(a, "RGBA")


def process(slug, src, scale=1.0):
    """Logoyu ortak bir kutuya, optik agirligi esitlenmis olarak yerlestirir.

    Tum ciktilar ayni en-boy oraninda oldugu icin sitede hepsi ayni boyutta
    gosterilir; gercek boyutu belirleyen sey kapladigi murekkep alani olur.
    Boylece uzun ince bir kelime logosu (Grundig) ile kare bir logo (LG)
    yan yana dengeli durur.
    """
    im = Image.open(src)
    im = strip_background(im)
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)

    ink = (np.array(im)[..., 3] > 8).sum()
    k = (TARGET_INK / ink) ** 0.5 * scale          # esit murekkep alani
    nw, nh = max(1, round(im.width * k)), max(1, round(im.height * k))
    # kutuya sigdir
    fit = min((BOX_W * 0.98) / nw, (BOX_H * 0.98) / nh, 1.0)
    nw, nh = max(1, round(nw * fit)), max(1, round(nh * fit))
    im = im.resize((nw, nh), Image.LANCZOS)

    canvas = Image.new("RGBA", (BOX_W, BOX_H), (0, 0, 0, 0))
    canvas.paste(im, ((BOX_W - nw) // 2, (BOX_H - nh) // 2), im)

    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, slug + ".png")
    canvas.save(dst, optimize=True)
    print("%-12s ic %4dx%-4d  kutu %dx%d  %6.1f KB" %
          (slug, nw, nh, BOX_W, BOX_H, os.path.getsize(dst) / 1024))


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        slug, rest = arg.split("=", 1)
        src, _, sc = rest.partition("@")
        process(slug, src, float(sc) if sc else 1.0)
