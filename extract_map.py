# -*- coding: utf-8 -*-
"""Turkiye il sinir verisinden Ege bolgesi haritasini uretir.

Kaynak: turkey-map-react (MIT, https://github.com/erdigokce/turkey-map-react)
Cikti : mapdata.py  (il path'leri + enlem/boylam -> SVG donusumu)
        assets_src/turkiye-ege.svg  (kucuk Turkiye konum haritasi)

Bu script bir kez calistirildi; ciktisi depoda. Yeniden calistirmak icin
turkey-map-react paketinin lib/data/index.js dosyasi gerekir.
"""
import re, os, json, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "/tmp/geo/tr_paths.json"
HERE = os.path.dirname(os.path.abspath(__file__))

# Ege haritasinda gosterilecek iller
FOCUS = ["izmir", "manisa", "aydin"]
CONTEXT = ["balikesir", "canakkale", "bursa", "kutahya", "usak",
           "afyonkarahisar", "denizli", "burdur", "mugla"]

# enlem/boylam -> kaynak SVG koordinati (bati illeri uzerinde en kucuk kareler
# ile bulundu, ardindan ilce konumlarinin dogru ile dusmesine gore ince ayar)
TX = {"ax": 51.7771, "bx": -1319.77, "ay": -70.4030, "by": 3101.26}

NUM = re.compile(r"-?\d+\.?\d*")


def round_path(d, nd=1):
    return NUM.sub(lambda m: ("%.*f" % (nd, float(m.group(0)))).rstrip("0").rstrip("."), d)


def coords(d):
    return [(float(a), float(b)) for a, b in re.findall(r"(-?\d+\.?\d*),(-?\d+\.?\d*)", d)]


def decimate(d, step=4, nd=1):
    """Bezier path'i, noktalarini seyrelterek poligona cevirir (konum haritasi icin)."""
    pts = coords(d)
    if len(pts) < 4:
        return None
    keep = pts[::step]
    if keep[-1] != pts[-1]:
        keep.append(pts[-1])
    if len(keep) < 3:
        return None
    f = "%." + str(nd) + "f"
    out = ["M" + f % keep[0][0] + " " + f % keep[0][1]]
    for x, y in keep[1:]:
        out.append("L" + f % x + " " + f % y)
    out.append("Z")
    return "".join(out)


def main():
    data = json.load(open(SRC, encoding="utf-8"))

    # --- bolge haritasi ---
    region = {}
    xs, ys = [], []
    for k in FOCUS + CONTEXT:
        d = data[k]["path"]
        region[k] = {"name": data[k]["name"], "d": round_path(d)}
        if k in FOCUS:                      # gorunum kutusu yalnizca odak illerden
            for x, y in coords(d):
                xs.append(x)
                ys.append(y)
    # komsu iller kadrajin disina tasar ve kirpilir; boylece kara tarafinda
    # bosluk kalmaz, bati tarafinda kalan bosluk gercek Ege kiyisidir
    padx, padt, padb = 16, 20, 16
    x0, x1 = min(xs) - padx, max(xs) + padx
    y0, y1 = min(ys) - padt, max(ys) + padb

    # --- Turkiye konum haritasi (ayri dosya, bir kez yuklenir) ---
    tx, ty = [], []
    for k, v in data.items():
        for x, y in coords(v["path"]):
            tx.append(x)
            ty.append(y)
    tpad = 6
    tvb = (min(tx) - tpad, min(ty) - tpad,
           max(tx) - min(tx) + 2 * tpad, max(ty) - min(ty) + 2 * tpad)
    parts = []
    for k, v in sorted(data.items()):
        p = decimate(v["path"])
        if not p:
            continue
        cls = "f" if k in FOCUS else "c"
        parts.append('<path class="%s" d="%s"/>' % (cls, p))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%.0f %.0f %.0f %.0f" '
           'role="img" aria-label="Türkiye üzerinde İzmir, Manisa ve Aydın">'
           '<title>Hizmet bölgemizin Türkiye üzerindeki konumu</title>'
           '<style>.c{fill:#E3E7EC;stroke:#fff;stroke-width:1.2}'
           '.f{fill:#E60034;stroke:#fff;stroke-width:1.2}</style>'
           '%s</svg>') % (tvb + (("".join(parts)),))
    out_svg = os.path.join(HERE, "assets_src", "turkiye-ege.svg")
    os.makedirs(os.path.dirname(out_svg), exist_ok=True)
    open(out_svg, "w", encoding="utf-8").write(svg)

    # --- mapdata.py ---
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Ege bolgesi il sinirlari ve enlem/boylam donusumu.',
        "",
        "extract_map.py tarafindan uretildi.",
        "Il sinir verisi: turkey-map-react (MIT) - https://github.com/erdigokce/turkey-map-react",
        '"""',
        "",
        "# enlem/boylam -> harita koordinati",
        "TX = %r" % TX,
        "",
        "# bolge haritasinin gorunum kutusu: (x, y, genislik, yukseklik)",
        "VIEWBOX = (%.1f, %.1f, %.1f, %.1f)" % (x0, y0, x1 - x0, y1 - y0),
        "",
        "FOCUS = %r" % FOCUS,
        "CONTEXT = %r" % CONTEXT,
        "",
        "PATHS = {",
    ]
    for k in FOCUS + CONTEXT:
        lines.append('    %r: {"name": %r, "d": %r},' % (k, region[k]["name"], region[k]["d"]))
    lines += ["}", "", "", "def project(lat, lon):", '    """Enlem/boylam degerini harita koordinatina cevirir."""',
              "    return (TX['ax'] * lon + TX['bx'], TX['ay'] * lat + TX['by'])", ""]
    open(os.path.join(HERE, "mapdata.py"), "w", encoding="utf-8").write("\n".join(lines))

    print("viewBox: %.1f %.1f %.1f %.1f" % (x0, y0, x1 - x0, y1 - y0))
    print("mapdata.py: %.1f KB" % (os.path.getsize(os.path.join(HERE, "mapdata.py")) / 1024))
    print("turkiye-ege.svg: %.1f KB" % (os.path.getsize(out_svg) / 1024))


if __name__ == "__main__":
    main()
