# -*- coding: utf-8 -*-
"""48 sayfalik statik siteyi, tek bir HTML dosyasinda gezilebilir onizlemeye cevirir.

- Tum sayfalarin <body> icerigi tek dosyaya gomulur
- Ic linkler hash router'a ("#/kategori/klima.html") cevrilir
- CSS ve JS bir kez inline edilir, logolar data: URI olur
- Ciktiya harici istek yok; tek dosya olarak her yerde acilir
"""
import os, re, json, base64, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(ROOT, "preview.html")

BODY_RE = re.compile(r"<body>(.*?)</body>", re.S)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
DESC_RE = re.compile(r'<meta name="description" content="(.*?)">', re.S)


def mime(path):
    ext = os.path.splitext(path)[1].lower()
    return {".png": "image/png", ".svg": "image/svg+xml", ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(ext, "application/octet-stream")


def data_uri(path):
    with open(path, "rb") as f:
        return "data:%s;base64,%s" % (mime(path), base64.b64encode(f.read()).decode())


def collect():
    pages = {}
    for root, _, files in os.walk(SITE):
        for f in files:
            if not f.endswith(".html"):
                continue
            full = os.path.join(root, f)
            key = os.path.relpath(full, SITE).replace(os.sep, "/")
            pages[key] = open(full, encoding="utf-8").read()
    return pages


def rewrite(key, doc, assets):
    """Bir sayfanin body'sini al, ic linkleri hash rotaya cevir, asset'leri gomule."""
    body = BODY_RE.search(doc).group(1)
    base = os.path.dirname(key)

    def fix_href(m):
        attr, q, href = m.group(1), m.group(2), m.group(3)
        if href.startswith(("http", "mailto:", "tel:", "data:", "#")):
            return m.group(0)
        frag = ""
        if "#" in href:
            href, frag = href.split("#", 1)
            frag = "#" + frag
        if not href:
            return m.group(0)
        target = os.path.normpath(os.path.join(base, href)).replace(os.sep, "/")
        if target.endswith(".html"):
            return '%s=%s#/%s%s%s' % (attr, q, target, frag, q)
        if target in assets:                      # gorseller: kanonik yol, JS cozer
            return '%s=%s%s%s' % (attr, q, target, q)
        return m.group(0)

    body = re.sub(r'\b(href|src)=(["\'])([^"\']+)\2', fix_href, body)
    # sayfa ici script etiketi (site.js) onizlemede bir kez yuklenecek
    body = re.sub(r'<script src="[^"]*site\.js"[^>]*></script>', "", body)
    return body


def main():
    pages = collect()
    css = open(os.path.join(SITE, "assets", "style.css"), encoding="utf-8").read()
    js = open(os.path.join(SITE, "assets", "site.js"), encoding="utf-8").read()

    assets = {}
    adir = os.path.join(SITE, "assets")
    for root, _, files in os.walk(adir):
        for f in files:
            if f.lower().endswith((".png", ".svg", ".jpg", ".jpeg", ".webp")):
                full = os.path.join(root, f)
                key = os.path.relpath(full, SITE).replace(os.sep, "/")
                assets[key] = data_uri(full)

    store, meta = {}, {}
    for key, doc in sorted(pages.items()):
        store[key] = rewrite(key, doc, assets)
        meta[key] = {
            "t": html.unescape(TITLE_RE.search(doc).group(1)),
            "d": html.unescape(DESC_RE.search(doc).group(1)),
        }

    nav_list = sorted(k for k in store if k != "404.html")
    out = """<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Odabaşı Dayanıklı Tüketim — Site Önizlemesi</title>
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap">
<style>
__CSS__

/* ---- sadece onizleme ---- */
.pv-bar{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:200;display:flex;
  align-items:center;gap:10px;background:rgba(11,12,15,.94);backdrop-filter:blur(10px);color:#fff;
  padding:8px 10px 8px 16px;border-radius:999px;box-shadow:0 12px 40px rgba(0,0,0,.32);
  font:500 13px/1 Inter,system-ui,sans-serif;max-width:calc(100vw - 32px)}
.pv-bar b{font-weight:700;letter-spacing:.02em;white-space:nowrap}
.pv-bar b i{font-style:normal;color:#E60034}
.pv-sep{width:1px;height:20px;background:rgba(255,255,255,.18)}
.pv-bar select{appearance:none;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);
  color:#fff;border-radius:999px;padding:8px 30px 8px 14px;font:500 13px Inter,system-ui,sans-serif;
  cursor:pointer;max-width:44vw;text-overflow:ellipsis}
.pv-bar select:focus{outline:2px solid #E60034;outline-offset:1px}
.pv-bar select option{background:#15171C;color:#fff}
.pv-arrow{position:absolute;right:22px;pointer-events:none;opacity:.6}
.pv-count{color:#8B95A3;white-space:nowrap}
@media (max-width:640px){.pv-bar{font-size:12px;padding:7px 8px 7px 13px}.pv-count{display:none}.pv-bar select{max-width:52vw}}
@media print{.pv-bar{display:none}}
</style>
</head>
<body>
<div id="pv-root"></div>

<div class="pv-bar" role="navigation" aria-label="Önizleme sayfa seçici">
  <b>ÖNİZLEME<i>.</i></b>
  <span class="pv-sep"></span>
  <span style="position:relative;display:inline-flex;align-items:center">
    <select id="pv-select" aria-label="Sayfa seç">__OPTIONS__</select>
    <svg class="pv-arrow" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
  </span>
  <span class="pv-count">__COUNT__ sayfa</span>
</div>

<script id="pv-data" type="application/json">__DATA__</script>
<script id="pv-meta" type="application/json">__META__</script>
<script id="pv-assets" type="application/json">__ASSETS__</script>
<script>
(function(){
  var PAGES = JSON.parse(document.getElementById('pv-data').textContent);
  var META  = JSON.parse(document.getElementById('pv-meta').textContent);
  var ASSETS = JSON.parse(document.getElementById('pv-assets').textContent);
  var root  = document.getElementById('pv-root');
  var sel   = document.getElementById('pv-select');

  function route(){
    var h = location.hash.replace(/^#\\/?/, '');
    if (!h || !PAGES[h]) h = 'index.html';
    root.innerHTML = PAGES[h];
    root.querySelectorAll('img[src]').forEach(function(img){
      var k = img.getAttribute('src');
      if (ASSETS[k]) img.src = ASSETS[k];
    });
    document.title = (META[h] ? META[h].t : 'Odabaşı') + ' — Önizleme';
    if (sel.value !== h) sel.value = h;
    initPage();
    window.scrollTo(0, 0);
  }

  sel.addEventListener('change', function(){ location.hash = '#/' + sel.value; });
  window.addEventListener('hashchange', route);

  // --- site.js davranislari, her sayfa degisiminde yeniden baglanir ---
  function initPage(){
__JS__
  }

  route();
})();
</script>
</body>
</html>"""

    options = "".join(
        '<option value="%s">%s</option>' % (html.escape(k), html.escape(label(k, meta)))
        for k in nav_list)

    out = (out.replace("__CSS__", css)
              .replace("__OPTIONS__", options)
              .replace("__COUNT__", str(len(nav_list)))
              .replace("__DATA__", json.dumps(store, ensure_ascii=False).replace("</", "<\\/"))
              .replace("__META__", json.dumps(meta, ensure_ascii=False).replace("</", "<\\/"))
              .replace("__ASSETS__", json.dumps(assets, ensure_ascii=False).replace("</", "<\\/"))
              .replace("__JS__", indent(js)))

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(out)
    print("preview.html: %d sayfa, %.2f MB" % (len(store), os.path.getsize(OUT) / 1048576))


def indent(js):
    return "\n".join("    " + line for line in js.strip().splitlines())


GROUP = {"kategori": "Ürün", "marka": "Marka", "bolge": "Bölge", "blog": "Blog"}


def label(key, meta):
    if key == "index.html":
        return "Ana Sayfa"
    parts = key.split("/")
    if len(parts) == 2:
        g = GROUP.get(parts[0], parts[0].title())
        if parts[1] == "index.html":
            return "Blog — Tüm yazılar"
        name = meta[key]["t"].split("|")[0].strip()
        return "%s — %s" % (g, name[:52])
    name = meta[key]["t"].split("|")[0].strip()
    return "Kurumsal — %s" % name[:52]


if __name__ == "__main__":
    main()
