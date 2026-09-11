# -*- coding: utf-8 -*-
"""Odabasi Dayanikli Tuketim - statik site uretici."""
import os, re, shutil, json, html
from data import SITE, BRANDS, CATEGORIES, LOCATIONS, POSTS, GENERAL_FAQS, BRANCHES
import mapdata

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

BRAND_BY = {b["slug"]: b for b in BRANDS}
CAT_BY = {c["slug"]: c for c in CATEGORIES}

# ---------------------------------------------------------------------------
# IKONLAR
# ---------------------------------------------------------------------------
ICONS = {
    "buzdolabi": '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M6 10h12"/><path d="M9 6v2"/><path d="M9 13v2"/>',
    "camasir-makinesi": '<rect x="3" y="2" width="18" height="20" rx="2"/><circle cx="12" cy="14" r="5"/><circle cx="12" cy="14" r="2"/><path d="M7 6h.01"/><path d="M11 6h.01"/>',
    "bulasik-makinesi": '<rect x="3" y="2" width="18" height="20" rx="2"/><path d="M3 7h18"/><path d="M8 12v6"/><path d="M12 12v6"/><path d="M16 12v6"/>',
    "kurutma-makinesi": '<rect x="3" y="2" width="18" height="20" rx="2"/><circle cx="12" cy="14" r="5"/><path d="M10 12c1 1 1 3 0 4"/><path d="M14 12c-1 1-1 3 0 4"/><path d="M7 6h.01"/>',
    "ankastre-set": '<rect x="3" y="8" width="18" height="13" rx="2"/><path d="M3 13h18"/><circle cx="7" cy="17" r="1"/><path d="M4 4h16"/><path d="M8 4v2"/><path d="M16 4v2"/>',
    "klima": '<rect x="2" y="4" width="20" height="8" rx="2"/><path d="M6 16c0 2 1 3 2 3"/><path d="M12 16c0 2 1 3 2 3"/><path d="M17 16c0 2 1 3 2 3"/><path d="M5 8h14"/>',
    "derin-dondurucu": '<rect x="2" y="6" width="20" height="12" rx="2"/><path d="M2 10h20"/><path d="M12 2v3"/><path d="M10 3l2-1 2 1"/>',
    "ticari-sogutma": '<rect x="4" y="2" width="16" height="20" rx="1"/><path d="M4 8h16"/><path d="M4 14h16"/><path d="M17 4v3"/><path d="M17 10v3"/><path d="M17 16v3"/>',
    "televizyon": '<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/>',
    "kucuk-ev-aletleri": '<path d="M6 3v7a4 4 0 0 0 8 0V3"/><path d="M10 14v7"/><path d="M18 3v18"/><path d="M18 3c2 2 2 6 0 8"/>',
    "temizlik-ekipmanlari": '<path d="M4 20h9"/><path d="M8 20V9"/><path d="M5 9h6l-1-6H6z"/><path d="M15 4h5v5"/><path d="M20 4l-6 6"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "truck": '<rect x="1" y="6" width="13" height="10" rx="1"/><path d="M14 9h4l3 3v4h-7z"/><circle cx="5.5" cy="18.5" r="1.8"/><circle cx="17.5" cy="18.5" r="1.8"/>',
    "shield": '<path d="M12 2l8 3v6c0 5-3.5 9.3-8 11-4.5-1.7-8-6-8-11V5z"/><path d="M9 12l2 2 4-4"/>',
    "tools": '<path d="M14.7 6.3a4 4 0 0 1 5 5L21 13l-3 3-9.5-9.5L11 4z"/><path d="M3 21l7-7"/>',
    "check": '<path d="M20 6L9 17l-5-5"/>',
    "chat": '<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 9 9 0 0 1-3.8-.8L3 21l1.9-5a8.3 8.3 0 0 1-.9-3.8 8.4 8.4 0 0 1 8.5-8.2A8.4 8.4 0 0 1 21 11.5z"/>',
    "arrow": '<path d="M5 12h14"/><path d="M13 5l7 7-7 7"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/><path d="M6 15h4"/>',
}


def icon(name, cls="ico"):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true">%s</svg>') % (cls, ICONS.get(name, ICONS["check"]))


def e(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------------------
# YOL YARDIMCILARI
# ---------------------------------------------------------------------------
def rel(depth):
    return "" if depth == 0 else "../" * depth


def url(path):
    return SITE["domain"].rstrip("/") + "/" + path.lstrip("/")


ALL_PAGES = []  # (path, priority, changefreq)


def register(path, priority="0.7", freq="monthly"):
    ALL_PAGES.append((path, priority, freq))


# ---------------------------------------------------------------------------
# ORTAK BLOKLAR
# ---------------------------------------------------------------------------
BRAND_LOGO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets_src", "markalar")
BRAND_LOGO_EXT = (".svg", ".png", ".webp", ".jpg")


def brand_logo_file(slug):
    """assets_src/markalar/<slug>.<ext> varsa dosya adini dondurur."""
    for ext in BRAND_LOGO_EXT:
        if os.path.exists(os.path.join(BRAND_LOGO_DIR, slug + ext)):
            return slug + ext
    return None


def brand_mark(depth, b, size="", fallback=True, text_only=False):
    """Marka logosu. Dosya yoksa: fallback True ise markanin adi, degilse hic basilmaz.

    text_only: koyu zeminli kartlar icin - logo yerine her zaman markanin adi.
    Logolarin cogu koyu zeminde siluete dondugu icin orada yazi daha iyi duruyor.
    """
    f = None if text_only else brand_logo_file(b["slug"])
    if not f and not fallback:
        return ""
    cls = "bmark" + (" " + size if size else "")
    if f:
        inner = ('<img src="%sassets/markalar/%s" alt="%s logosu" loading="lazy" decoding="async">'
                 % (rel(depth), f, e(b["name"])))
    else:
        inner = '<span class="bmark-word">%s</span>' % e(b["name"])
    return '<span class="%s">%s</span>' % (cls, inner)


def brand_wall(depth, slugs=None, title=True):
    items = []
    ordered = [b for b in BRANDS if b["authorized"]] + [b for b in BRANDS if not b["authorized"]]
    for b in ordered:
        if slugs and b["slug"] not in slugs:
            continue
        cls = "bwall-item"
        if b["authorized"]:
            cls += " is-auth"
        if not brand_logo_file(b["slug"]):
            cls += " is-nologo"
        items.append(
            '<a class="%s" href="%smarka/%s.html" aria-label="%s ürünleri">'
            '%s<span class="bwall-name">%s</span>%s</a>'
            % (cls, rel(depth), b["slug"], e(b["name"]),
               brand_mark(depth, b), e(b["name"]),
               '<span class="bwall-tag">Yetkili Bayi</span>' if b["authorized"] else ""))
    return '<div class="bwall">%s</div>' % "".join(items)


def logo(depth, variant=""):
    r = rel(depth)
    src = "assets/logo-white.png" if variant == "white" else "assets/logo.png"
    return ('<a class="logo" href="%sindex.html" aria-label="%s ana sayfa">'
            '<img src="%s%s" alt="%s logosu" width="480" height="142" %s>'
            '</a>') % (r, e(SITE["name"]), r, src, e(SITE["name"]),
                       'loading="lazy"' if variant == "white" else "")


def nav(depth, active=""):
    r = rel(depth)
    cat_links = "".join(
        '<a href="%skategori/%s.html">%s %s</a>' % (r, c["slug"], icon(c["slug"], "ico sm"), e(c["name"]))
        for c in CATEGORIES)
    brand_links = "".join(
        '<a href="%smarka/%s.html">%s%s</a>' % (
            r, b["slug"], e(b["name"]),
            '<span class="tag">Yetkili Bayi</span>' if b["authorized"] else "")
        for b in BRANDS)
    loc_links = "".join(
        '<a href="%sbolge/%s.html">%s</a>' % (r, l["slug"], e(l["name"]))
        for l in LOCATIONS)
    return """
<nav class="nav" id="nav">
  <div class="has-menu">
    <button class="nav-link nav-toggle%s" aria-expanded="false">Ürünler %s</button>
    <div class="mega mega-cats">%s</div>
  </div>
  <div class="has-menu">
    <button class="nav-link nav-toggle%s" aria-expanded="false">Markalar %s</button>
    <div class="mega mega-brands">%s</div>
  </div>
  <div class="has-menu">
    <button class="nav-link nav-toggle%s" aria-expanded="false">Bölgeler %s</button>
    <div class="mega mega-locs">%s</div>
  </div>
  <a class="nav-link%s" href="%sservis-ve-destek.html">Servis</a>
  <a class="nav-link%s" href="%sblog/index.html">Blog</a>
  <a class="nav-link%s" href="%shakkimizda.html">Hakkımızda</a>
  <a class="nav-link%s" href="%siletisim.html">İletişim</a>
</nav>""" % (
        " is-active" if active == "kategori" else "", chevron(), cat_links,
        " is-active" if active == "marka" else "", chevron(), brand_links,
        " is-active" if active == "bolge" else "", chevron(), loc_links,
        " is-active" if active == "servis" else "", r,
        " is-active" if active == "blog" else "", r,
        " is-active" if active == "hakkimizda" else "", r,
        " is-active" if active == "iletisim" else "", r,
    )


def chevron():
    return ('<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>')


def header(depth, active=""):
    return """
<a class="skip" href="#main">İçeriğe geç</a>
<div class="topbar">
  <div class="wrap topbar-in">
    <span>%s İzmir, Aydın ve Manisa'ya teslimat ve montaj</span>
    <span class="topbar-mid">%s Ücretsiz teslimat</span>
    <span class="topbar-mid">%s Ücretsiz montaj</span>
    <span class="topbar-r">%s</span>
  </div>
</div>
<header class="hd">
  <div class="wrap hd-in">
    %s
    %s
    <div class="hd-cta">
      <a class="btn btn-ghost" href="tel:%s">%s %s</a>
      <a class="btn btn-primary" href="%siletisim.html">Teklif Al</a>
      <button class="burger" id="burger" aria-label="Menü" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>""" % (
        icon("truck", "ico sm"), icon("check", "ico sm"), icon("check", "ico sm"),
        e(SITE["hours"]),
        logo(depth), nav(depth, active),
        e(SITE["phone_tel"]), icon("phone", "ico sm"), e(SITE["phone_display"]),
        rel(depth),
    )


PERKS = [
    ("truck", "Ücretsiz teslimat", "İzmir, Aydın ve Manisa'ya ürününüzü ücretsiz teslim ediyoruz."),
    ("tools", "Ücretsiz montaj", "Kurulum, bağlantı ve devreye alma ücretsiz. Ek malzeme çıkarsa önceden söyleriz."),
    ("card", "Taksit imkanı", "Anlaşmalı bankaların kredi kartlarına taksit seçenekleri sunuyoruz."),
    ("shield", "Yetkili bayi", "LG, Uğur ve Altus yetkili bayisiyiz. Tüm ürünler Türkiye distribütör garantili."),
]


def perks_band(compact=False):
    items = "".join(
        '<div class="perk">%s<div><strong>%s</strong>%s</div></div>'
        % (icon(i, "ico lg"), e(t), "" if compact else "<span>%s</span>" % e(d))
        for i, t, d in PERKS)
    return ('<section class="perks%s"><div class="wrap perks-in">%s</div></section>'
            % (" perks-compact" if compact else "", items))


def branch_line(b):
    """Subenin tek satirlik adresi."""
    bits = [x for x in [b.get("street"), b.get("area"), b.get("district")] if x]
    return ", ".join(bits) + " / " + b["city"] if bits else b["city"]


def branch_cards(depth, compact=False):
    r = rel(depth)
    out = []
    for b in BRANCHES:
        brand = BRAND_BY.get(b["brand"])
        mark = brand_mark(depth, brand, "bmark-sm") if brand else ""
        tel = ('<a class="br-tel" href="tel:%s">%s %s</a>'
               % (e(b["phone_tel"]), icon("phone", "ico sm"), e(b["phone_display"]))) if b.get("phone_tel") else (
              '<a class="br-tel" href="tel:%s">%s %s</a>'
              % (e(SITE["phone_tel"]), icon("phone", "ico sm"), e(SITE["phone_display"])))
        maps = ('<a class="br-map" href="%s" target="_blank" rel="noopener">%s Haritada aç</a>'
                % (e(b["maps"]), icon("pin", "ico sm"))) if b.get("maps") else ""
        note = "" if compact else "<p>%s</p>" % e(b["note"])
        link = ('<a class="br-brand" href="%smarka/%s.html">%s ürünleri %s</a>'
                % (r, b["brand"], e(brand["name"]), icon("arrow", "ico sm"))) if brand and not compact else ""
        out.append(
            '<div class="branch"><div class="br-head">%s<div><strong>%s</strong>'
            '<span>%s</span></div></div>%s<div class="br-links">%s%s%s</div></div>'
            % (mark, e(b["name"]), e(branch_line(b)), note, tel, maps, link))
    return '<div class="branches%s">%s</div>' % (" branches-compact" if compact else "", "".join(out))


def auth_names(last=" ve "):
    names = [b["name"] for b in BRANDS if b["authorized"]]
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + last + names[-1]


def ask_first(depth):
    r = rel(depth)
    return """
<section class="ask">
  <div class="wrap ask-in">
    <div class="ask-copy">
      <p class="eyebrow">%s Yetkili Bayisi</p>
      <h2>%s almadan önce bize sorun</h2>
      <p>Başka bir yerden fiyat aldıysanız, karar vermeden önce bir telefon edin. Yetkili bayi olduğumuz için
      bu markalarda size ne sunabileceğimizi tek aramada net söyleriz: fiyat, teslimat tarihi, montaj
      ve garanti dahil. Aradaki farkı görmeden almayın.</p>
      <ul class="ask-list">
        <li>%s İzmir'de iki marka mağazamız var: LG Shop Çankaya ve Uğur Shop Eşrefpaşa</li>
        <li>%s Aldığınız teklifi bize iletin, üzerine ne verebileceğimizi söyleyelim</li>
        <li>%s Teslimat ve montaj ücretsiz, fiyata ek kalem çıkmaz</li>
        <li>%s Garanti ve servis kaydı yetkili bayi üzerinden açılır</li>
      </ul>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="tel:%s">%s %s</a>
        <a class="btn btn-outline btn-lg" href="%siletisim.html">Teklifinizi gönderin</a>
      </div>
    </div>
    <div class="ask-brands">%s</div>
  </div>
</section>""" % (auth_names(" ve "), auth_names(" veya "),
                 icon("check", "ico sm"), icon("check", "ico sm"),
                 icon("check", "ico sm"), icon("check", "ico sm"),
                 e(SITE["phone_tel"]), icon("phone", "ico sm"), e(SITE["phone_display"]), r,
                 "".join(
                     '<a class="ask-brand" href="%smarka/%s.html">%s<span>Yetkili Bayi</span></a>'
                     % (r, x["slug"], brand_mark(depth, x, "bmark-lg"))
                     for x in BRANDS if x["authorized"]))


def footer(depth):
    r = rel(depth)
    cats = "".join('<li><a href="%skategori/%s.html">%s</a></li>' % (r, c["slug"], e(c["name"])) for c in CATEGORIES)
    brands = "".join('<li><a href="%smarka/%s.html">%s</a></li>' % (r, b["slug"], e(b["name"])) for b in BRANDS)
    locs = "".join('<li><a href="%sbolge/%s.html">%s</a></li>' % (r, l["slug"], e(l["name"])) for l in LOCATIONS)
    return """
<footer class="ft">
  <div class="wrap ft-in">
    <div class="ft-col ft-brand">
      %s
      <p class="ft-desc">LG, Uğur ve Altus yetkili bayisi. İzmir, Aydın ve Manisa'da beyaz eşya, ankastre, klima ve
      ticari soğutma. Ücretsiz teslimat, ücretsiz montaj ve taksit imkanı.</p>
      <address class="ft-addr">
        <span class="ft-br"><b>LG Shop Çankaya</b>Çankaya, Konak / İzmir</span>
        <span class="ft-br"><b>Uğur Shop Eşrefpaşa</b>Eşrefpaşa, Konak / İzmir</span>
        <a href="tel:%s">%s</a>
        <a href="mailto:%s">%s</a>
        <span>%s</span>
      </address>
    </div>
    <div class="ft-col"><h3>Ürün Grupları</h3><ul>%s</ul></div>
    <div class="ft-col"><h3>Markalar</h3><ul>%s</ul></div>
    <div class="ft-col"><h3>Hizmet Bölgeleri</h3><ul>%s</ul></div>
    <div class="ft-col">
      <h3>Kurumsal</h3>
      <ul>
        <li><a href="%shakkimizda.html">Hakkımızda</a></li>
        <li><a href="%sservis-ve-destek.html">Servis ve Destek</a></li>
        <li><a href="%ssikca-sorulan-sorular.html">Sıkça Sorulan Sorular</a></li>
        <li><a href="%sblog/index.html">Blog</a></li>
        <li><a href="%siletisim.html">İletişim</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap ft-bot">
    <span>&copy; %s %s. Tüm hakları saklıdır.</span>
    <span>Son güncelleme: %s</span>
  </div>
</footer>
<a class="wa" href="https://wa.me/%s" target="_blank" rel="noopener" aria-label="WhatsApp ile yazın">%s<span>WhatsApp</span></a>
<script src="%sassets/site.js" defer></script>""" % (
        logo(depth, "white"),
        e(SITE["phone_tel"]), e(SITE["phone_display"]),
        e(SITE["email"]), e(SITE["email"]), e(SITE["hours"]),
        cats, brands, locs,
        r, r, r, r, r,
        "2026", e(SITE["name"]), e(SITE["updated"]),
        e(SITE["whatsapp"]), icon("chat", "ico"), r,
    )


def crumbs(depth, items):
    """items: [(label, href|None)]"""
    r = rel(depth)
    parts = ['<a href="%sindex.html">Ana Sayfa</a>' % r]
    for label, href in items:
        if href:
            parts.append('<a href="%s%s">%s</a>' % (r, href, e(label)))
        else:
            parts.append('<span aria-current="page">%s</span>' % e(label))
    return '<nav class="crumbs" aria-label="Site yolu"><div class="wrap">%s</div></nav>' % (
        '<span class="sep" aria-hidden="true">/</span>'.join(parts))


def crumb_ld(items):
    ls = [{"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": url("index.html")}]
    for i, (label, href) in enumerate(items, start=2):
        entry = {"@type": "ListItem", "position": i, "name": label}
        if href:
            entry["item"] = url(href)
        ls.append(entry)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ls}


def answer_box(text, label="Kısa cevap"):
    return ('<div class="answer" data-answer><span class="answer-label">%s</span>'
            '<p>%s</p></div>') % (e(label), e(text))


def faq_html(faqs, title="Sıkça Sorulan Sorular"):
    items = "".join(
        '<details class="faq-item"><summary><span>%s</span>%s</summary><div class="faq-a"><p>%s</p></div></details>'
        % (e(q), '<svg class="plus" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>', e(a))
        for q, a in faqs)
    return '<section class="sec faq"><div class="wrap"><h2>%s</h2><div class="faq-list">%s</div></div></section>' % (e(title), items)


def faq_ld(faqs):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }


def table_html(t):
    head = "".join("<th>%s</th>" % e(h) for h in t["head"])
    rows = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % e(c) for c in r) for r in t["rows"])
    return ('<div class="table-wrap"><table><caption>%s</caption>'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>') % (e(t["caption"]), head, rows)


def cta_band(depth, title, text, ):
    r = rel(depth)
    return """
<section class="band">
  <div class="wrap band-in">
    <div>
      <h2>%s</h2>
      <p>%s</p>
    </div>
    <div class="band-actions">
      <a class="btn btn-primary btn-lg" href="tel:%s">%s Hemen Ara</a>
      <a class="btn btn-outline btn-lg" href="%siletisim.html">Fiyat Teklifi Al</a>
    </div>
  </div>
</section>""" % (e(title), e(text), e(SITE["phone_tel"]), icon("phone", "ico sm"), r)


def cat_card(depth, c):
    r = rel(depth)
    return ('<a class="card cat-card" href="%skategori/%s.html">'
            '<span class="card-ico">%s</span>'
            '<span class="card-body"><strong>%s</strong><span>%s</span></span>'
            '<span class="card-go">%s</span></a>') % (
        r, c["slug"], icon(c["slug"], "ico lg"), e(c["name"]),
        e(", ".join(BRAND_BY[b]["name"] for b in c["brands"][:4])), icon("arrow", "ico sm"))


def brand_chip(depth, b):
    r = rel(depth)
    return ('<a class="chip" href="%smarka/%s.html"><strong>%s</strong>%s</a>') % (
        r, b["slug"], e(b["name"]),
        '<span class="tag">Yetkili Bayi</span>' if b["authorized"] else "")


def loc_chip(depth, l):
    r = rel(depth)
    return '<a class="chip" href="%sbolge/%s.html">%s%s</a>' % (
        r, l["slug"], icon("pin", "ico sm"), e(l["name"]))


def lead_form(depth, source=""):
    opts = "".join('<option value="%s">%s</option>' % (e(c["name"]), e(c["name"])) for c in CATEGORIES)
    return """
<form class="lead" id="leadForm" data-source="%s" novalidate>
  <div class="lead-row">
    <label>Ad Soyad<input type="text" name="ad" required autocomplete="name" placeholder="Adınız ve soyadınız"></label>
    <label>Telefon<input type="tel" name="tel" required autocomplete="tel" placeholder="05xx xxx xx xx"></label>
  </div>
  <div class="lead-row">
    <label>İlgilendiğiniz ürün grubu<select name="urun"><option value="">Seçiniz</option>%s<option value="Diğer">Diğer</option></select></label>
    <label>Bölge<select name="bolge"><option value="">Seçiniz</option>%s</select></label>
  </div>
  <label>Notunuz<textarea name="not" rows="3" placeholder="Model, adet veya özel talebiniz varsa yazabilirsiniz"></textarea></label>
  <button class="btn btn-primary btn-lg" type="submit">Teklif İste</button>
  <p class="lead-note">Formu gönderdiğinizde talebiniz WhatsApp üzerinden mağazamıza iletilir. Dilerseniz doğrudan <a href="tel:%s">%s</a> numarasından da ulaşabilirsiniz.</p>
</form>""" % (e(source), opts,
              "".join('<option value="%s">%s</option>' % (e(l["name"]), e(l["name"])) for l in LOCATIONS),
              e(SITE["phone_tel"]), e(SITE["phone_display"]))



# ---------------------------------------------------------------------------
# HIZMET BOLGELERI HARITASI
# ---------------------------------------------------------------------------
# Il sinirlari mapdata.py'den gelir (kaynak: turkey-map-react, MIT).
# Ilceler gercek enlem/boylam degerleriyle yerlestirilir.
MAP_POINTS = [
    # (il, ad, enlem, boylam, bolge sayfasi slug'i veya None)
    ("İzmir", "Menemen", 38.60, 27.07, "izmir-menemen"),
    ("İzmir", "Çiğli", 38.50, 27.07, "izmir-cigli"),
    ("İzmir", "Karşıyaka", 38.46, 27.12, None),
    ("İzmir", "Bornova", 38.47, 27.22, "izmir-bornova"),
    ("İzmir", "Kemalpaşa", 38.42, 27.42, None),
    ("İzmir", "Konak", 38.42, 27.13, "izmir"),
    ("İzmir", "Buca", 38.39, 27.17, "izmir-buca"),
    ("İzmir", "Karabağlar", 38.37, 27.10, "izmir-karabaglar"),
    ("İzmir", "Balçova", 38.39, 27.05, None),
    ("İzmir", "Narlıdere", 38.39, 27.00, None),
    ("İzmir", "Gaziemir", 38.32, 27.12, "izmir-gaziemir"),
    ("İzmir", "Menderes", 38.25, 27.13, None),
    ("İzmir", "Torbalı", 38.16, 27.36, "izmir-torbali"),
    ("Manisa", "Soma", 39.19, 27.61, None),
    ("Manisa", "Akhisar", 38.92, 27.84, None),
    ("Manisa", "Saruhanlı", 38.73, 27.57, None),
    ("Manisa", "Manisa Merkez", 38.61, 27.43, "manisa"),
    ("Manisa", "Turgutlu", 38.50, 27.70, "manisa-turgutlu"),
    ("Manisa", "Salihli", 38.48, 28.14, "manisa-salihli"),
    ("Manisa", "Alaşehir", 38.35, 28.52, None),
    ("Aydın", "Nazilli", 37.91, 28.32, "aydin-nazilli"),
    ("Aydın", "Germencik", 37.87, 27.60, None),
    ("Aydın", "Kuşadası", 37.86, 27.26, "aydin-kusadasi"),
    ("Aydın", "Aydın Merkez", 37.85, 27.84, "aydin"),
    ("Aydın", "İncirliova", 37.85, 27.72, None),
    ("Aydın", "Söke", 37.75, 27.41, None),
    ("Aydın", "Çine", 37.61, 28.06, None),
    ("Aydın", "Didim", 37.38, 27.27, None),
]

PROV_KEY = {"İzmir": "izmir", "Manisa": "manisa", "Aydın": "aydin"}
PROV_TINT = {"İzmir": "#E60034", "Manisa": "#12507E", "Aydın": "#1F7A4D"}
# il adi etiketinin il merkezine gore kaydirilmasi (nokta yiginlarindan kacinmak icin)
PROV_LABEL_OFF = {"İzmir": (-2, 33), "Manisa": (11, -2), "Aydın": (7, 11)}

_NUMPAIR = re.compile(r"(-?\d+\.?\d*),(-?\d+\.?\d*)")


def _centroid(d):
    pts = [(float(a), float(b)) for a, b in _NUMPAIR.findall(d)]
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def service_map(depth, active=None):
    r = rel(depth)
    vb = mapdata.VIEWBOX
    provinces = ["İzmir", "Manisa", "Aydın"]

    land = "".join('<path class="smap-land" d="%s"><title>%s</title></path>'
                   % (mapdata.PATHS[k]["d"], e(mapdata.PATHS[k]["name"]))
                   for k in mapdata.CONTEXT)

    focus, labels = [], []
    for prov in provinces:
        k = PROV_KEY[prov]
        d = mapdata.PATHS[k]["d"]
        focus.append('<path class="smap-prov-area" d="%s" style="--tint:%s"><title>%s</title></path>'
                     % (d, PROV_TINT[prov], e(prov)))
        cx, cy = _centroid(d)
        ox, oy = PROV_LABEL_OFF[prov]
        labels.append('<text class="smap-prov" x="%.1f" y="%.1f" fill="%s">%s</text>'
                      % (cx + ox, cy + oy, PROV_TINT[prov], e(prov.upper())))

    dots = []
    for prov, name, lat, lon, slug in MAP_POINTS:
        if not slug:
            continue
        x, y = mapdata.project(lat, lon)
        is_hub = slug in ("izmir", "aydin", "manisa")
        cls = "smap-dot" + (" is-hub" if is_hub else "") + (" is-active" if slug == active else "")
        dots.append('<a href="%sbolge/%s.html" class="smap-hit" data-loc="%s">'
                    '<circle class="%s" cx="%.1f" cy="%.1f" r="%s"><title>%s</title></circle></a>'
                    % (r, slug, e(slug), cls, x, y, "3.4" if is_hub else "2.4", e(name)))

    sx, sy = mapdata.project(float(SITE["lat"]), float(SITE["lng"]))
    store = ('<g class="smap-store" transform="translate(%.1f %.1f)">'
             '<circle class="smap-pulse" r="8"/><circle r="4.4"/><circle class="smap-core" r="1.7"/>'
             '<title>%s</title></g>' % (sx, sy, e(SITE["name"])))

    km50 = abs(mapdata.TX["ay"]) * (50.0 / 111.0)
    scale = ('<g class="smap-scale" transform="translate(%.1f %.1f)">'
             '<path d="M0 0 H%.1f M0 -2 V2 M%.1f -2 V2"/>'
             '<text x="%.1f" y="8">50 km</text></g>'
             % (vb[0] + 10, vb[1] + vb[3] - 12, km50, km50, km50 / 2))
    north = ('<g class="smap-north" transform="translate(%.1f %.1f)">'
             '<path d="M0 -7 L2.6 2.6 L0 0.6 L-2.6 2.6 Z"/><text x="0" y="9">K</text></g>'
             % (vb[0] + vb[2] - 12, vb[1] + 14))
    sea = ""

    lists = []
    for prov in provinces:
        items = []
        for p in MAP_POINTS:
            if p[0] != prov:
                continue
            name, slug = p[1], p[4]
            if slug:
                items.append('<li><a href="%sbolge/%s.html" data-loc="%s"%s>%s</a></li>'
                             % (r, slug, e(slug), ' class="is-active"' if slug == active else "", e(name)))
            else:
                items.append('<li><span>%s</span></li>' % e(name))
        lists.append(
            '<div class="smap-group"><h3><span class="smap-key" style="background:%s"></span>%s</h3>'
            '<ul>%s</ul></div>' % (PROV_TINT[prov], e(prov), "".join(items)))

    return """
<section class="sec sec-soft smap-sec">
  <div class="wrap">
    <div class="sec-head">
      <h2>Hizmet verdiğimiz bölgeler</h2>
      <p>İzmir merkezliyiz; Aydın ve Manisa il ve ilçelerine de ücretsiz teslimat ve ücretsiz montaj
      hizmeti veriyoruz. Haritadaki ilçelere tıklayarak o bölgeye özel sayfayı açabilirsiniz.</p>
    </div>
    <div class="smap">
      <figure class="smap-fig">
        <svg viewBox="%.1f %.1f %.1f %.1f" role="img"
             aria-label="Ege bölgesi haritası: İzmir, Manisa ve Aydın hizmet bölgeleri">
          <title>Odabaşı Dayanıklı Tüketim hizmet bölgeleri — Ege bölgesi</title>
          <rect class="smap-water" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>
          %s
          <g class="smap-focus">%s</g>
          %s
          %s
          %s
          <g class="smap-dots">%s</g>
          %s
          %s
        </svg>
        <img class="smap-inset" src="%sassets/turkiye-ege.svg" alt="Hizmet bölgesinin Türkiye üzerindeki konumu"
             width="150" height="66" loading="lazy" decoding="async">
        <figcaption>İl sınırları gerçek sınır verisinden, ilçeler gerçek koordinatlarından çizildi.
        Listede olmayan bir adres için mağazamızı arayabilirsiniz.</figcaption>
      </figure>
      <div class="smap-side">
        <div class="smap-legend">
          <span><i class="lg-store"></i>Mağazalarımız (2 şube)</span>
          <span><i class="lg-hub"></i>İl merkezi</span>
          <span><i class="lg-dot"></i>Teslimat ve montaj</span>
        </div>
        %s
        <a class="btn btn-primary" href="tel:%s">%s Bölgeniz için arayın</a>
      </div>
    </div>
  </div>
</section>""" % (vb[0], vb[1], vb[2], vb[3],
                 vb[0], vb[1], vb[2], vb[3],
                 land, "".join(focus), sea, "".join(labels), store,
                 "".join(dots), scale, north, r,
                 "".join(lists), e(SITE["phone_tel"]), icon("phone", "ico sm"))


# ---------------------------------------------------------------------------
# SCHEMA
# ---------------------------------------------------------------------------
def postal_ld():
    a = {"@type": "PostalAddress", "addressCountry": "TR",
         "addressLocality": SITE["district"] or SITE["city"],
         "addressRegion": SITE["city"]}
    if SITE.get("street"):
        a["streetAddress"] = SITE["street"]
    if SITE.get("postal"):
        a["postalCode"] = SITE["postal"]
    return a


def local_business_ld():
    return {
        "@context": "https://schema.org",
        "@type": ["Store", "HomeGoodsStore"],
        "@id": url("#store"),
        "name": SITE["name"],
        "alternateName": "Odabaşı Beyaz Eşya",
        "description": "İzmir, Aydın ve Manisa'da beyaz eşya, ankastre, klima ve ticari soğutma satışı. LG, Uğur ve Altus yetkili bayisi. Ücretsiz teslimat, ücretsiz montaj ve taksit imkanı.",
        "url": SITE["domain"] + "/",
        "telephone": SITE["phone_tel"],
        "email": SITE["email"],
        "priceRange": "$$",
        "currenciesAccepted": "TRY",
        "paymentAccepted": "Nakit, Kredi Kartı, Havale",
        "foundingDate": SITE["founded"],
        "address": postal_ld(),
        "geo": {"@type": "GeoCoordinates", "latitude": SITE["lat"], "longitude": SITE["lng"]},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": SITE["hours_schema"][0],
            "opens": SITE["hours_schema"][1],
            "closes": SITE["hours_schema"][2],
        }],
        "areaServed": [{"@type": "City", "name": l["name"]} for l in LOCATIONS],
        "brand": [{"@type": "Brand", "name": b["name"]} for b in BRANDS],
        "sameAs": [SITE["instagram"], SITE["facebook"]],
        "department": [{"@id": url("iletisim.html#%s" % b["slug"])} for b in BRANCHES],
        "location": [{"@id": url("iletisim.html#%s" % b["slug"])} for b in BRANCHES],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Ürün Grupları",
            "itemListElement": [
                {"@type": "OfferCatalog", "name": c["name"],
                 "url": url("kategori/%s.html" % c["slug"])} for c in CATEGORIES
            ],
        },
    }


def branch_ld():
    """Her sube icin ayri Store kaydi; ana isletmeye bagli."""
    out = []
    for b in BRANCHES:
        addr = {"@type": "PostalAddress", "addressCountry": "TR",
                "addressLocality": b["district"], "addressRegion": b["city"]}
        if b.get("street"):
            addr["streetAddress"] = b["street"]
        if b.get("postal"):
            addr["postalCode"] = b["postal"]
        node = {
            "@context": "https://schema.org", "@type": ["Store", "HomeGoodsStore"],
            "@id": url("iletisim.html#%s" % b["slug"]),
            "name": "%s — %s" % (SITE["name"], b["name"]),
            "alternateName": b["name"],
            "description": b["note"],
            "url": url("iletisim.html"),
            "telephone": b.get("phone_tel") or SITE["phone_tel"],
            "email": SITE["email"],
            "address": addr,
            "parentOrganization": {"@id": url("#store")},
            "openingHoursSpecification": [{
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": SITE["hours_schema"][0],
                "opens": SITE["hours_schema"][1],
                "closes": SITE["hours_schema"][2],
            }],
        }
        if b.get("maps"):
            node["hasMap"] = b["maps"]
        out.append(node)
    return out


def website_ld():
    return {
        "@context": "https://schema.org", "@type": "WebSite",
        "@id": url("#website"), "url": SITE["domain"] + "/",
        "name": SITE["name"], "inLanguage": "tr-TR",
        "publisher": {"@id": url("#store")},
    }


# ---------------------------------------------------------------------------
# SAYFA ISKELETI
# ---------------------------------------------------------------------------
def render(path, title, desc, body, ld=None, active="", depth=None, og_type="website"):
    if depth is None:
        depth = path.count("/")
    r = rel(depth)
    ld = ld or []
    body = body.replace("{{PERKS}}", perks_band(True)).replace("{{ASK}}", ask_first(depth))
    body = body.replace("{{BRANCHES}}", branch_cards(depth))
    body = body.replace("{{ASK_IF}}", "")
    ld_html = "".join(
        '<script type="application/ld+json">%s</script>'
        % json.dumps(x, ensure_ascii=False, separators=(",", ":")) for x in ld)
    doc = """<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="%s">
<meta name="geo.region" content="TR-35">
<meta name="geo.placename" content="%s">
<meta name="geo.position" content="%s;%s">
<meta name="ICBM" content="%s, %s">
<meta property="og:type" content="%s">
<meta property="og:site_name" content="%s">
<meta property="og:locale" content="tr_TR">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<meta name="theme-color" content="#E60034">
<link rel="icon" href="%sassets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="%sassets/style.css">
%s
</head>
<body>
%s
<main id="main">
%s
</main>
%s
</body>
</html>""" % (
        e(title), e(desc), url(path), e(SITE["name"]),
        e(SITE["address_line"]),
        e(SITE["lat"]), e(SITE["lng"]), e(SITE["lat"]), e(SITE["lng"]),
        e(og_type), e(SITE["name"]), e(title), e(desc), url(path),
        e(title), e(desc), r, r, ld_html,
        header(depth, active), body, footer(depth),
    )
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(doc)


# ---------------------------------------------------------------------------
# ANA SAYFA
# ---------------------------------------------------------------------------
def build_home():
    cats = "".join(cat_card(0, c) for c in CATEGORIES)
    brands = brand_wall(0)
    posts = "".join(
        '<a class="post-card" href="blog/%s.html"><span class="post-cat">%s</span>'
        '<h3>%s</h3><p>%s</p><span class="post-date">%s</span></a>'
        % (p["slug"], e(p["cat"]), e(p["title"]), e(p["desc"]), e(tr_date(p["date"])))
        for p in POSTS[:3])

    home_faqs = GENERAL_FAQS[:6]

    body = """
<section class="hero">
  <div class="wrap hero-in">
    <div class="hero-copy">
      <p class="eyebrow">%s LG, Uğur ve Altus Yetkili Bayisi</p>
      <h1>Beyaz eşyada <em>uygun fiyat,</em> kaliteli ürün</h1>
      <p class="lead-p">İzmir, Aydın ve Manisa'da on markanın beyaz eşya, ankastre, klima ve ticari soğutma
      ürünlerini tek noktadan alın. Teslimat ve montaj ücretsiz, taksit imkanı var.</p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="tel:%s">%s %s</a>
        <a class="btn btn-outline btn-lg" href="#teklif">Fiyat Teklifi Al</a>
      </div>
      <ul class="hero-points">
        <li>%s Ücretsiz teslimat</li>
        <li>%s Ücretsiz montaj</li>
        <li>%s Taksit imkanı</li>
        <li>%s Türkiye distribütör garantisi</li>
      </ul>
    </div>
    <div class="hero-art">%s</div>
  </div>
</section>
%s
%s

<section class="sec">
  <div class="wrap">
    %s
  </div>
</section>

<section class="sec" id="urunler">
  <div class="wrap">
    <div class="sec-head">
      <h2>Ürün grupları</h2>
      <p>Ev tipi beyaz eşyadan işletmelere yönelik ticari soğutmaya kadar tüm ürün gruplarımız.</p>
    </div>
    <div class="grid cards">%s</div>
  </div>
</section>

<section class="sec sec-soft" id="markalar">
  <div class="wrap">
    <div class="sec-head">
      <h2>Satışını yaptığımız markalar</h2>
      <p>LG, Uğur ve Altus yetkili bayisiyiz. Bunun yanında yedi markanın ürünlerini Türkiye distribütör garantisi kapsamında satıyoruz.</p>
    </div>
    %s
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Neden Odabaşı?</h2></div>
    <div class="grid feats">
      <div class="feat">%s<h3>Ücretsiz teslimat ve montaj</h3><p>Ürün fiyatına teslimat ve standart montaj dahildir. Ek malzeme gerekirse keşifte önceden bildiririz; teslimat gününde sürpriz kalem çıkmaz.</p></div>
      <div class="feat">%s<h3>Yetkili bayi güvencesi</h3><p>LG, Uğur ve Altus yetkili bayisiyiz. Satılan tüm ürünler Türkiye distribütör garantisi kapsamındadır; garanti belgesi teslimatla birlikte düzenlenir.</p></div>
      <div class="feat">%s<h3>Taksit imkanı</h3><p>Anlaşmalı bankaların kredi kartlarına taksit seçenekleri sunuyoruz. Güncel kampanyalar için mağazamızı arayabilirsiniz.</p></div>
      <div class="feat">%s<h3>Ticari soğutma çözümleri</h3><p>Uğur yetkili bayisi olarak market, kafe, restoran ve pastaneler için reyon dolabı, şişe soğutucu ve teşhir üniteleri sunuyoruz. Mağaza planınıza göre yerleşim önerisi hazırlıyoruz.</p></div>
    </div>
  </div>
</section>

%s

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Satın alma rehberleri</h2><p>Doğru ürünü seçmenize yardımcı olacak pratik rehberler.</p></div>
    <div class="grid posts">%s</div>
    <p class="more"><a href="blog/index.html">Tüm yazıları görün %s</a></p>
  </div>
</section>

<section class="sec sec-dark" id="teklif">
  <div class="wrap form-split">
    <div>
      <h2>Fiyat teklifi alın</h2>
      <p>İhtiyacınızı yazın, uygun modelleri ve güncel fiyatları birlikte değerlendirelim. Toplu alım ve ticari projeler için de aynı formu kullanabilirsiniz.</p>
      <ul class="contact-list">
        <li>%s<a href="tel:%s">%s</a></li>
        <li>%s<span>%s</span></li>
      </ul>
      %s
    </div>
    <div class="form-card">%s</div>
  </div>
</section>
%s
""" % (
        icon("shield", "ico sm"), e(SITE["phone_tel"]), icon("phone", "ico sm"), e(SITE["phone_display"]),
        icon("check", "ico sm"), icon("check", "ico sm"), icon("check", "ico sm"), icon("check", "ico sm"),
        HERO_ART,
        perks_band(),
        ask_first(0),
        answer_box("Odabaşı Dayanıklı Tüketim, İzmir merkezli bir beyaz eşya ve dayanıklı tüketim mağazasıdır. "
                   "LG, Uğur ve Altus yetkili bayisi olup Hoover, TCL, Electrolux, Şenocak, Grundig, Kärcher ve Rota "
                   "ürünlerini de satmaktadır. İzmir, Aydın ve Manisa'da ücretsiz teslimat, ücretsiz montaj ve "
                   "taksit imkanı sunulmaktadır.",
                   "Odabaşı Dayanıklı Tüketim nedir?"),
        cats, brands,
        icon("truck", "ico lg"), icon("shield", "ico lg"), icon("card", "ico lg"), icon("ticari-sogutma", "ico lg"),
        service_map(0), posts, icon("arrow", "ico sm"),
        icon("phone", "ico sm"), e(SITE["phone_tel"]), e(SITE["phone_display"]),
        icon("check", "ico sm"), e(SITE["hours"]),
        branch_cards(0, compact=True),
        lead_form(0, "Ana sayfa"),
        faq_html(home_faqs),
    )

    render("index.html",
           "İzmir Beyaz Eşya | LG, Uğur, Altus Yetkili Bayi | Odabaşı",
           "İzmir, Aydın ve Manisa'da beyaz eşya, ankastre, klima ve ticari soğutma. LG, Uğur ve Altus yetkili bayisi. Ücretsiz teslimat, ücretsiz montaj, taksit imkanı.",
           body,
           ld=[local_business_ld(), website_ld(), faq_ld(home_faqs)] + branch_ld(),
           active="home", depth=0)
    register("index.html", "1.0", "weekly")


def tr_date(iso):
    months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
              "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    y, m, d = iso.split("-")
    return "%d %s %s" % (int(d), months[int(m) - 1], y)


# ---------------------------------------------------------------------------
# KATEGORI SAYFALARI
# ---------------------------------------------------------------------------
def build_categories():
    for c in CATEGORIES:
        path = "kategori/%s.html" % c["slug"]
        cb = [("Ürünler", None), (c["name"], None)]
        secs = "".join(
            '<section class="prose-sec"><h2>%s</h2>%s</section>'
            % (e(h), "".join("<p>%s</p>" % e(p) for p in ps))
            for h, ps in c["sections"])
        tbl = table_html(c["table"]) if c.get("table") else ""
        brands = brand_wall(1, set(c["brands"]))
        others = "".join(cat_card(1, x) for x in CATEGORIES if x["slug"] != c["slug"])

        body = """
%s
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">%s Ürün Grubu</p>
    <h1>%s Modelleri ve Fiyatları</h1>
    <p class="lead-p">%s</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="tel:%s">%s Fiyat sor</a>
      <a class="btn btn-outline" href="../iletisim.html">Teklif al</a>
    </div>
  </div>
</section>
{{PERKS}}
<section class="sec"><div class="wrap prose">
  %s
  %s
  %s
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head"><h2>%s ürünlerinde çalıştığımız markalar</h2></div>
  <div class="chips">%s</div>
</div></section>
%s
%s
%s
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head"><h2>Diğer ürün grupları</h2></div>
  <div class="grid cards">%s</div>
</div></section>
""" % (
            crumbs(1, cb),
            e(c["name"]), e(c["name"]), e(c["intro"]),
            e(SITE["phone_tel"]), icon("phone", "ico sm"),
            answer_box(c["answer"], "%s seçiminde kısa cevap" % c["name"]),
            secs, tbl,
            e(c["name"]), brands,
            cta_band(1, "%s için doğru modeli birlikte seçelim" % c["name"],
                     "İhtiyacınızı anlatın, uygun modelleri ve güncel fiyatları karşılaştırmalı sunalım. Teslimat ve montaj ücretsiz, taksit imkanı var."),
            service_map(1),
            faq_html(c["faqs"], "%s hakkında sıkça sorulan sorular" % c["name"]),
            others,
        )

        ld = [
            crumb_ld(cb), faq_ld(c["faqs"]), local_business_ld(),
            {"@context": "https://schema.org", "@type": "CollectionPage",
             "name": "%s Modelleri" % c["name"],
             "url": url(path), "inLanguage": "tr-TR",
             "about": {"@type": "Thing", "name": c["name"]},
             "isPartOf": {"@id": url("#website")},
             "mainEntity": {
                 "@type": "ItemList",
                 "name": "%s markaları" % c["name"],
                 "itemListElement": [
                     {"@type": "ListItem", "position": i, "name": BRAND_BY[b]["name"],
                      "url": url("marka/%s.html" % b)}
                     for i, b in enumerate(c["brands"], 1)],
             }},
        ]
        render(path, c["title"].format(site=SITE["short"]), c["desc"], body, ld=ld,
               active="kategori", depth=1)
        register(path, "0.9", "weekly")


# ---------------------------------------------------------------------------
# MARKA SAYFALARI
# ---------------------------------------------------------------------------
def build_brands():
    for b in BRANDS:
        path = "marka/%s.html" % b["slug"]
        cb = [("Markalar", None), (b["name"], None)]
        lines = "".join(
            '<div class="line"><strong>%s</strong><p>%s</p></div>' % (e(n), e(d))
            for n, d in b["lines"])
        bodyp = "".join("<p>%s</p>" % e(p) for p in b["body"])
        cats = "".join(cat_card(1, CAT_BY[s]) for s in b["cats"] if s in CAT_BY)
        others = brand_wall(1, set(x["slug"] for x in BRANDS if x["slug"] != b["slug"]))
        locs = "".join(loc_chip(1, l) for l in LOCATIONS if l["hub"])
        badge = '<span class="badge">Yetkili Bayi</span>' if b["authorized"] else '<span class="badge badge-alt">Türkiye Garantili</span>'

        body = """
%s
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">%s %s</p>
    <div class="brand-head">%s<h1>%s%s</h1></div>
    <p class="lead-p">%s</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="tel:%s">%s Fiyat sor</a>
      <a class="btn btn-outline" href="../iletisim.html">Teklif al</a>
    </div>
  </div>
</section>
{{PERKS}}
<section class="sec"><div class="wrap prose">
  %s
  %s
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head"><h2>%s ürün grupları</h2></div>
  <div class="grid lines">%s</div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>%s ürünlerini bulabileceğiniz kategoriler</h2></div>
  <div class="grid cards">%s</div>
</div></section>
%s
%s
{{ASK_IF}}
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head"><h2>%s ürünlerinde teslimat bölgelerimiz</h2></div>
  <div class="chips">%s</div>
  <div class="sec-head" style="margin-top:48px"><h2>Diğer markalar</h2></div>
  %s
</div></section>
""" % (
            crumbs(1, cb),
            e(b["name"]), "Yetkili Bayi" if b["authorized"] else "Ürünleri",
            brand_mark(1, b, "bmark-xl", fallback=False),
            e(b["name"]), badge, e(b["intro"]),
            e(SITE["phone_tel"]), icon("phone", "ico sm"),
            answer_box(b["answer"], "%s hakkında kısa cevap" % b["name"]),
            bodyp,
            e(b["name"]), lines,
            e(b["name"]), cats,
            cta_band(1, "%s ürünlerinde güncel fiyat alın" % b["name"],
                     "Model listesi ve stok durumu için mağazamızı arayın ya da teklif formunu doldurun. Teslimat ve montaj ücretsiz."),
            faq_html(b["faqs"], "%s hakkında sıkça sorulan sorular" % b["name"]),
            e(b["name"]), locs, others,
        )

        ld = [
            crumb_ld(cb), faq_ld(b["faqs"]), local_business_ld(),
            {"@context": "https://schema.org", "@type": "CollectionPage",
             "name": "%s Ürünleri" % b["name"], "url": url(path), "inLanguage": "tr-TR",
             "isPartOf": {"@id": url("#website")},
             "about": {"@type": "Brand", "name": b["name"]},
             "mainEntity": {
                 "@type": "ItemList",
                 "itemListElement": [
                     {"@type": "ListItem", "position": i, "name": n}
                     for i, (n, d) in enumerate(b["lines"], 1)],
             }},
        ]
        body = body.replace("{{ASK_IF}}", ask_first(1) if b["authorized"] else "")
        render(path, b["title"].format(site=SITE["short"]), b["desc"], body, ld=ld,
               active="marka", depth=1)
        register(path, "0.9", "monthly")


# ---------------------------------------------------------------------------
# LOKASYON SAYFALARI
# ---------------------------------------------------------------------------
def build_locations():
    for l in LOCATIONS:
        path = "bolge/%s.html" % l["slug"]
        cb = [("Bölgeler", None), (l["name"], None)]
        name = l["name"]
        il = l["il"]
        where = name if l["hub"] else "%s, %s" % (name, il)
        areas = "".join('<li>%s</li>' % e(a) for a in l["areas"])
        cats = "".join(cat_card(1, c) for c in CATEGORIES)
        brands = brand_wall(1)

        answer = ("%s bölgesinde beyaz eşya, ankastre, klima ve ticari soğutma ihtiyaçlarınız için "
                  "Odabaşı Dayanıklı Tüketim hizmet vermektedir. LG, Uğur ve Altus yetkili bayisi olarak "
                  "%s ve çevresine teslimat, montaj ve devreye alma hizmeti sunuyoruz." % (where, name))

        faqs = [
            ("%s'ya beyaz eşya teslimatı yapıyor musunuz?" % name,
             "Evet. %s ve çevresine beyaz eşya teslimatı ve montajı yapıyoruz. Stokta bulunan ürünlerde teslimat "
             "genellikle 1-3 iş günü içinde tamamlanır; özel sipariş ürünlerde süre tedarik takvimine göre değişir." % name),
            ("%s'da montaj hizmeti veriyor musunuz?" % name,
             "Evet. Çamaşır ve bulaşık makinesi bağlantısı, klima montajı, ankastre yerleşimi ve ticari soğutma "
             "devreye alma işlemlerini %s bölgesinde de gerçekleştiriyoruz. Klima ve ankastre montajında keşif sonrası "
             "ek malzeme ihtiyacı netleştirilir." % name),
            ("%s'daki işletmeler için ticari soğutma çözümü sunuyor musunuz?" % name,
             "Evet. Uğur yetkili bayisi olarak %s bölgesindeki market, kafe, restoran ve pastanelere şişe soğutucu, "
             "reyon dolabı, dondurma kabini ve teşhir ünitesi tedarik ediyoruz. Mağaza planınızı paylaşırsanız "
             "yerleşim önerisiyle birlikte teklif hazırlıyoruz." % name),
            ("%s için hangi markaların ürünlerini alabilirim?" % name,
             "LG, Uğur ve Altus yetkili bayisiyiz. Ayrıca Hoover, TCL, Electrolux, Şenocak, Grundig, Kärcher ve Rota "
             "ürünlerini Türkiye distribütör garantisi kapsamında satıyoruz. Tüm markalarda %s bölgesine teslimat "
             "yapılmaktadır." % name),
        ]

        body = """
%s
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">%s Hizmet Bölgesi</p>
    <h1>%s Beyaz Eşya, Ankastre ve Klima</h1>
    <p class="lead-p">%s</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="tel:%s">%s %s</a>
      <a class="btn btn-outline" href="../iletisim.html">Teklif al</a>
    </div>
  </div>
</section>
{{PERKS}}
<section class="sec"><div class="wrap prose">
  %s
  <section class="prose-sec">
    <h2>%s'da beyaz eşya ihtiyacı</h2>
    <p>%s</p>
    <p>Odabaşı Dayanıklı Tüketim olarak %s bölgesine buzdolabı, çamaşır makinesi, bulaşık makinesi, kurutma makinesi,
    ankastre set, klima, derin dondurucu, televizyon ve ticari soğutma ürünleri tedarik ediyoruz. Teslimat, kata çıkarma
    ve montaj süreçleri tek bir randevuyla planlanır.</p>
  </section>
  <section class="prose-sec">
    <h2>%s'da hizmet verdiğimiz mahalle ve bölgeler</h2>
    <ul class="areas">%s</ul>
    <p>Listede yer almayan bir adres için de teslimat yapılıp yapılamayacağını mağazamızı arayarak öğrenebilirsiniz.</p>
  </section>
  <section class="prose-sec">
    <h2>%s'da teslimat ve montaj süreci</h2>
    <ol class="steps">
      <li><strong>İhtiyaç görüşmesi.</strong> Telefonla veya mağazada ihtiyacınızı netleştiriyoruz; ölçü, kapasite ve bütçe birlikte değerlendiriliyor.</li>
      <li><strong>Teklif ve onay.</strong> Uygun modeller güncel fiyatlarıyla sunuluyor. Toplu alımlarda adet bazlı fiyatlandırma yapılıyor.</li>
      <li><strong>Teslimat planlaması.</strong> Adres, kat, asansör ve kapı ölçüsü bilgileri alınarak teslimat günü belirleniyor.</li>
      <li><strong>Kurulum ve devreye alma.</strong> Ürün yerine yerleştiriliyor, bağlantıları yapılıyor ve çalışır durumda teslim ediliyor.</li>
      <li><strong>Garanti ve servis.</strong> Garanti belgesi düzenleniyor; sonraki servis taleplerinde süreci mağaza olarak takip ediyoruz.</li>
    </ol>
  </section>
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head"><h2>%s'da satışını yaptığımız ürün grupları</h2></div>
  <div class="grid cards">%s</div>
</div></section>
%s
<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>%s'da bulabileceğiniz markalar</h2></div>
  %s
</div></section>
%s
{{ASK}}
%s
""" % (
            crumbs(1, cb), e(where), e(where), e(l["note"]),
            e(SITE["phone_tel"]), icon("phone", "ico sm"), e(SITE["phone_display"]),
            answer_box(answer, "%s hizmet bölgesi" % name),
            e(name), e(l["note"]), e(name),
            e(name), areas,
            e(name),
            e(name), cats,
            cta_band(1, "%s'da mı yaşıyorsunuz?" % name,
                     "Teslimat ve montaj ücretsiz. Takvim için mağazamızı arayın, aynı gün bilgi verelim."),
            e(name), brands,
            faq_html(faqs, "%s beyaz eşya hakkında sıkça sorulan sorular" % name),
            service_map(1, l["slug"]),
        )

        ld = [
            crumb_ld(cb), faq_ld(faqs),
            {"@context": "https://schema.org", "@type": ["Store", "HomeGoodsStore"],
             "name": "%s - %s" % (SITE["name"], name),
             "url": url(path),
             "description": "%s bölgesinde beyaz eşya, ankastre, klima ve ticari soğutma satışı, teslimat ve montaj." % name,
             "telephone": SITE["phone_tel"], "email": SITE["email"],
             "parentOrganization": {"@id": url("#store")},
             "address": postal_ld(),
             "areaServed": [{"@type": "Place", "name": a} for a in l["areas"]],
             "geo": {"@type": "GeoCoordinates", "latitude": SITE["lat"], "longitude": SITE["lng"]},
             },
        ]
        title = "%s Beyaz Eşya | Buzdolabı, Klima, Ankastre | %s" % (name, SITE["short"])
        desc = ("%s beyaz eşya, ankastre set, klima ve ticari soğutma. LG, Uğur ve Altus yetkili bayisi "
                "Odabaşı'dan ücretsiz teslimat ve montaj." % where)
        render(path, title, desc, body, ld=ld, active="bolge", depth=1)
        register(path, "0.8", "monthly")


# ---------------------------------------------------------------------------
# BLOG
# ---------------------------------------------------------------------------
def build_blog():
    cards = "".join(
        '<a class="post-card" href="%s.html"><span class="post-cat">%s</span>'
        '<h3>%s</h3><p>%s</p><span class="post-date">%s</span></a>'
        % (p["slug"], e(p["cat"]), e(p["title"]), e(p["desc"]), e(tr_date(p["date"])))
        for p in POSTS)
    cb = [("Blog", None)]
    body = """
%s
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Blog</p>
    <h1>Beyaz eşya satın alma rehberleri</h1>
    <p class="lead-p">Buzdolabı litresinden klima BTU hesabına, enerji etiketinden ticari soğutucu seçimine kadar
    karar vermenizi kolaylaştıracak pratik rehberler.</p>
  </div>
</section>
<section class="sec"><div class="wrap"><div class="grid posts">%s</div></div></section>
%s
""" % (crumbs(1, cb), cards,
       cta_band(1, "Aradığınız cevabı bulamadıysanız",
                "Mağazamızı arayın, ihtiyacınıza uygun modeli birlikte belirleyelim."))
    render("blog/index.html",
           "Beyaz Eşya Rehberleri ve Blog | %s" % SITE["short"],
           "Buzdolabı seçimi, klima BTU hesabı, enerji sınıfları, ankastre set ve ticari soğutucu rehberleri. Odabaşı Dayanıklı Tüketim blog.",
           body, ld=[crumb_ld(cb), local_business_ld()], active="blog", depth=1)
    register("blog/index.html", "0.7", "weekly")

    for p in POSTS:
        path = "blog/%s.html" % p["slug"]
        pcb = [("Blog", "blog/index.html"), (p["title"], None)]
        toc = "".join('<li><a href="#%s">%s</a></li>' % (slugify(h), e(h)) for h, _ in p["sections"])
        secs = "".join(
            '<section class="prose-sec" id="%s"><h2>%s</h2>%s</section>'
            % (slugify(h), e(h), "".join("<p>%s</p>" % e(x) for x in ps))
            for h, ps in p["sections"])
        related = "".join(cat_card(1, CAT_BY[s]) for s in p.get("related", []) if s in CAT_BY)
        more = "".join(
            '<a class="post-card" href="%s.html"><span class="post-cat">%s</span><h3>%s</h3>'
            '<span class="post-date">%s</span></a>' % (o["slug"], e(o["cat"]), e(o["title"]), e(tr_date(o["date"])))
            for o in POSTS if o["slug"] != p["slug"])[:100000]

        body = """
%s
<article class="article">
  <div class="wrap article-head">
    <p class="eyebrow">%s</p>
    <h1>%s</h1>
    <p class="meta">Yayın tarihi: <time datetime="%s">%s</time> &middot; %s</p>
  </div>
  <div class="wrap prose">
    %s
    <nav class="toc"><h2>İçindekiler</h2><ol>%s</ol></nav>
    %s
  </div>
</article>
%s
%s
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head"><h2>İlgili ürün grupları</h2></div>
  <div class="grid cards">%s</div>
  <div class="sec-head" style="margin-top:48px"><h2>Diğer yazılar</h2></div>
  <div class="grid posts">%s</div>
</div></section>
""" % (
            crumbs(1, pcb), e(p["cat"]), e(p["title"]),
            e(p["date"]), e(tr_date(p["date"])), e(SITE["name"]),
            answer_box(p["answer"], "Kısa cevap"),
            toc, secs,
            faq_html(p["faqs"], "Sıkça sorulan sorular"),
            cta_band(1, "Modeli birlikte seçelim",
                     "Rehberdeki kriterlere göre size uygun modelleri mağazamızda karşılaştırmalı gösterelim."),
            related, more,
        )

        ld = [
            crumb_ld(pcb), faq_ld(p["faqs"]),
            {"@context": "https://schema.org", "@type": "BlogPosting",
             "headline": p["title"], "description": p["desc"],
             "datePublished": p["date"], "dateModified": SITE["updated"],
             "inLanguage": "tr-TR", "url": url(path),
             "mainEntityOfPage": {"@type": "WebPage", "@id": url(path)},
             "author": {"@type": "Organization", "name": SITE["name"], "url": SITE["domain"] + "/"},
             "publisher": {"@id": url("#store")},
             "articleSection": p["cat"],
             "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["[data-answer]", "h1"]},
             },
        ]
        ptitle = p["title"] if len(p["title"]) > 50 else "%s | %s" % (p["title"], SITE["short"])
        render(path, ptitle, p["desc"], body, ld=ld,
               active="blog", depth=1, og_type="article")
        register(path, "0.6", "monthly")


def slugify(s):
    tr = {"ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u",
          "Ç": "c", "Ğ": "g", "İ": "i", "Ö": "o", "Ş": "s", "Ü": "u"}
    out = []
    for ch in s.lower():
        ch = tr.get(ch, ch)
        if ch.isalnum():
            out.append(ch)
        elif ch in " -_":
            out.append("-")
    return "-".join(x for x in "".join(out).split("-") if x)[:60]


# ---------------------------------------------------------------------------
# KURUMSAL SAYFALAR
# ---------------------------------------------------------------------------
def build_static():
    # --- Hakkimizda ---
    cb = [("Hakkımızda", None)]
    body = """
%s
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Hakkımızda</p>
    <h1>Odabaşı Dayanıklı Tüketim</h1>
    <p class="lead-p">İzmir merkezli bir beyaz eşya ve dayanıklı tüketim mağazasıyız. LG, Uğur ve Altus yetkili bayisi olarak
    ev tipi beyaz eşyadan işletmelere yönelik ticari soğutmaya kadar geniş bir ürün ailesini tek noktadan sunuyoruz.
    Teslimat ve montaj ücretsiz, taksit imkanı var.</p>
  </div>
</section>
{{PERKS}}
<section class="sec"><div class="wrap prose">
  %s
  <section class="prose-sec">
    <h2>Ne yapıyoruz?</h2>
    <p>Odabaşı Dayanıklı Tüketim, İzmir, Aydın ve Manisa'da beyaz eşya, ankastre mutfak ürünleri, klima, televizyon,
    küçük ev aletleri, temizlik ekipmanları ve ticari soğutma ürünlerinin satışını yapmaktadır. Satışın yanı sıra
    teslimat, kata çıkarma, montaj ve ticari ekipmanlarda devreye alma hizmetlerini de yürütüyoruz. Teslimat ve
    standart montaj ücretsizdir; anlaşmalı bankaların kredi kartlarına taksit imkanı sunuyoruz.</p>
    <p>Çalıştığımız markalar; LG, Uğur ve Altus (yetkili bayilik) ile Hoover, TCL, Electrolux, Şenocak, Grundig,
    Kärcher ve Rota. Tüm ürünler Türkiye distribütör garantisi kapsamındadır.</p>
  </section>
  <section class="prose-sec">
    <h2>Nasıl çalışıyoruz?</h2>
    <p>Beyaz eşya satın alma kararının çoğu zaman fiyat karşılaştırmasından ibaret olmadığını biliyoruz. Doğru litre,
    doğru kapasite, doğru BTU ve doğru ölçü seçilmediğinde ürün ne kadar iyi olursa olsun kullanıcı memnun olmuyor.
    Bu nedenle satış öncesinde ihtiyacı netleştirmeye zaman ayırıyoruz.</p>
    <p>Ankastre projelerde mutfak imalatından önce ölçü kontrolü yapıyoruz. Klima satışında oda büyüklüğü, cephe yönü
    ve cam yüzeyine göre BTU hesabı çıkarıyoruz. Ticari soğutmada mağaza planına göre reyon yerleşimi öneriyoruz.</p>
  </section>
  <section class="prose-sec">
    <h2>Kimlere hizmet veriyoruz?</h2>
    <ul class="ticks">
      <li>Ev kuran ve beyaz eşya yenileyen haneler</li>
      <li>Mutfak yenileyen ve ankastre set arayan kullanıcılar</li>
      <li>Market, bakkal, kafe, büfe, pastane ve restoran işletmeleri</li>
      <li>Toplu konut, site ve otel projeleri için toplu alım yapan kurumlar</li>
      <li>Kiralık daire ve yazlık donatan mülk sahipleri</li>
    </ul>
  </section>
  <section class="prose-sec">
    <h2>Şubelerimiz</h2>
    <p>İzmir'de iki marka mağazamız var. İkisi de Konak'ta, birbirine yakın mesafede.</p>
    {{BRANCHES}}
  </section>
  <section class="prose-sec">
    <h2>Hizmet bölgelerimiz</h2>
    <p>İzmir'in tüm merkez ilçeleri ile Aydın ve Manisa il ve ilçelerine ücretsiz teslimat ve ücretsiz montaj
    hizmeti veriyoruz. Mesafeye bağlı özel durumlar sipariş sırasında netleştirilir.</p>
  </section>
</div></section>
{{ASK}}
%s
%s
""" % (crumbs(0, cb),
       answer_box("Odabaşı Dayanıklı Tüketim, İzmir merkezli bir beyaz eşya ve dayanıklı tüketim mağazasıdır. "
                  "LG, Uğur ve Altus yetkili bayisi olarak buzdolabı, çamaşır makinesi, ankastre set, klima ve ticari "
                  "soğutma ürünlerini İzmir, Aydın ve Manisa'da satış, teslimat ve montaj hizmetiyle sunar.",
                  "Odabaşı Dayanıklı Tüketim kimdir?"),
       cta_band(0, "Mağazamıza bekleriz", "Ürünleri yerinde görmek için mağazamızı ziyaret edebilir ya da telefonla bilgi alabilirsiniz."),
       faq_html(GENERAL_FAQS[:5], "Bizimle ilgili sık sorulanlar"))
    render("hakkimizda.html",
           "Hakkımızda | Odabaşı Dayanıklı Tüketim | İzmir Beyaz Eşya",
           "Odabaşı Dayanıklı Tüketim; İzmir, Aydın ve Manisa'da beyaz eşya, ankastre, klima ve ticari soğutma satışı yapan LG, Uğur ve Altus yetkili bayisidir.",
           body, ld=[crumb_ld(cb), local_business_ld(), faq_ld(GENERAL_FAQS[:5])] + branch_ld(),
           active="hakkimizda", depth=0)
    register("hakkimizda.html", "0.7")

    # --- Servis ve destek ---
    cb = [("Servis ve Destek", None)]
    body = """
%s
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Servis ve Destek</p>
    <h1>Teslimat, montaj, garanti ve servis</h1>
    <p class="lead-p">Teslimat ve standart montaj ücretsizdir. Satış sonrasında ne olacağı çoğu zaman ürünün
    kendisi kadar önemli; teslimattan garanti sürecine kadar nasıl çalıştığımızı burada açıklıyoruz.</p>
  </div>
</section>
{{PERKS}}
<section class="sec"><div class="wrap prose">
  %s
  <section class="prose-sec">
    <h2>Teslimat — ücretsiz</h2>
    <p>İzmir merkez ve ilçeleri ile Aydın ve Manisa il ve ilçelerine teslimat ücretsizdir; ürün fiyatına dahildir. Stokta bulunan ürünlerde
    teslimat genellikle 1-3 iş günü içinde tamamlanır. Özel sipariş ürünlerde süre marka tedarik takvimine bağlıdır.</p>
    <p>Teslimat planlaması yaparken kat, asansör iç ölçüsü ve kapı genişliği bilgisini alıyoruz. Özellikle gardırop
    tipi buzdolapları ve büyük ticari ekipmanlarda bu ölçüler, teslimat gününde sürpriz yaşanmaması için kritik.</p>
  </section>
  <section class="prose-sec">
    <h2>Montaj kapsamı — ücretsiz</h2>
    <p>Standart montaj ücretsizdir; aşağıdaki işlemler için ayrıca ücret alınmaz. Yalnızca ek malzeme gerektiren
    durumlar (fazladan bakır boru, dış ünite konsolu, cephe çalışması) keşifte önceden bildirilir.</p>
    <ul class="ticks">
      <li><strong>Çamaşır ve bulaşık makinesi:</strong> yerine yerleştirme, nakliye cıvatalarının sökülmesi, su giriş ve tahliye bağlantısı.</li>
      <li><strong>Buzdolabı ve derin dondurucu:</strong> yerine yerleştirme, ayak ayarı, kapı yönü değişimi (model destekliyorsa).</li>
      <li><strong>Klima:</strong> iç ve dış ünite montajı, bakır boru çekimi, vakumlama, drenaj hattı ve test. Ücretsiz standart montaj belirli bir boru uzunluğunu kapsar; ek boru ve konsol ayrıca değerlendirilir.</li>
      <li><strong>Ankastre:</strong> fırın ve ocak yerleşimi, davlumbaz montajı. Gazlı ocaklarda gaz bağlantısı yetkili tesisatçı tarafından yapılır.</li>
      <li><strong>Ticari soğutma:</strong> yerine yerleştirme, seviye ayarı, devreye alma ve sıcaklık ayarı.</li>
    </ul>
  </section>
  <section class="prose-sec">
    <h2>Taksit imkanı</h2>
    <p>Anlaşmalı bankaların kredi kartlarına taksit seçenekleri sunuyoruz. Taksit sayıları banka kampanyalarına
    göre dönemsel olarak değiştiği için güncel bilgiyi mağazamızdan teyit etmenizi öneriyoruz. Toplu alım ve
    ticari projelerde ödeme planı ayrıca görüşülebilir.</p>
  </section>
  <section class="prose-sec">
    <h2>Garanti</h2>
    <p>Mağazamızdan satılan tüm ürünler Türkiye distribütör garantisi kapsamındadır. Garanti belgesi teslimatla
    birlikte düzenlenir. Beyaz eşyada standart garanti süresi genellikle 3 yıldır; ürün grubuna ve markaya göre
    değişebilir. Bazı modellerde motor veya kompresör için ek garanti tanımlanır.</p>
    <p>Garanti belgesini ve faturayı saklamanızı öneriyoruz; servis talebinde ilk istenen belgeler bunlardır.</p>
  </section>
  <section class="prose-sec">
    <h2>Arıza ve servis talebi</h2>
    <p>Garanti kapsamındaki arızalarda markanın yetkili servis ağı devreye girer. Mağaza olarak süreci takip ediyor,
    gerektiğinde yönlendirme yapıyoruz. Garanti dışı durumlarda da servise erişim konusunda destek sağlıyoruz.</p>
    <p>Ticari soğutma ekipmanlarında arıza, doğrudan ürün kaybı anlamına geldiği için bu grupta servis takibini
    öncelikli yürütüyoruz.</p>
  </section>
  <section class="prose-sec">
    <h2>Periyodik bakım önerileri</h2>
    <ul class="ticks">
      <li><strong>Buzdolabı:</strong> arka ızgara ve kondenser tozunun yılda 1-2 kez temizlenmesi; kapı contası kontrolü.</li>
      <li><strong>Çamaşır makinesi:</strong> filtre temizliği (2-3 ayda bir), 90 derece boş program ile kazan temizliği.</li>
      <li><strong>Bulaşık makinesi:</strong> filtre temizliği, tuz ve parlatıcı seviyesi kontrolü.</li>
      <li><strong>Klima:</strong> sezon boyunca 2-4 haftada bir iç ünite filtresi yıkama; yılda bir genel bakım (tercihen mayıs).</li>
      <li><strong>Ticari soğutma:</strong> kondenser temizliği (tozlu ortamda aylık, normalde 3 ayda bir), conta kontrolü.</li>
    </ul>
  </section>
</div></section>
%s
%s
""" % (crumbs(0, cb),
       answer_box("Mağazamızdan satılan ürünlerde teslimat, standart montaj ve garanti belgesi düzenleme "
                  "hizmetlerini biz yürütüyoruz. Garanti kapsamındaki arızalarda markanın yetkili servis ağı devreye "
                  "girer; süreci mağaza olarak takip ediyoruz. İzmir, Aydın ve Manisa'da hizmet veriyoruz.",
                  "Servis ve destek kapsamı"),
       cta_band(0, "Servis veya montaj talebiniz mi var?",
                "Mağazamızı arayın; ürün, model ve arıza bilgisini alarak süreci başlatalım."),
       faq_html([
           ("Montaj ücreti ürün fiyatına dahil mi?",
            "Evet, standart montaj ücretsizdir ve ürün fiyatına dahildir. Klima montajında standart bakır boru "
            "uzunluğunu aşan durumlar, dış ünite konsolu, cephe çalışması ve elektrik hattı çekimi ek malzeme kalemi "
            "oluşturur; bunlar keşif sırasında önceden ve net olarak bildirilir."),
           ("Eski cihazımı söküp götürüyor musunuz?",
            "Yeni ürün teslimatında eski cihazın yerinden alınması konusunda destek sağlıyoruz. Koşullar ürün grubuna ve "
            "adrese göre değişebildiği için sipariş sırasında netleştiriyoruz."),
           ("Kapı yönü değişimi yapılıyor mu?",
            "Buzdolaplarının çoğunda kapı açılış yönü değiştirilebilir. Bu işlem, modelin buna uygun tasarlanmış olmasına "
            "bağlıdır ve teslimat sırasında ekibimiz tarafından yapılabilir."),
           ("Garanti belgemi kaybettim, ne yapmalıyım?",
            "Fatura, garanti kaydına ulaşmak için genellikle yeterlidir. Mağazamızı aradığınızda satış kaydınız üzerinden "
            "gerekli bilgileri sağlayabiliriz."),
       ], "Servis hakkında sıkça sorulan sorular"))
    render("servis-ve-destek.html",
           "Servis, Montaj ve Garanti | Odabaşı Dayanıklı Tüketim",
           "Beyaz eşya teslimat, montaj, garanti ve servis süreçleri. İzmir, Aydın ve Manisa'da kurulum, devreye alma ve periyodik bakım önerileri.",
           body, ld=[crumb_ld(cb), local_business_ld()], active="servis", depth=0)
    register("servis-ve-destek.html", "0.7")

    # --- SSS ---
    cb = [("Sıkça Sorulan Sorular", None)]
    allf = list(GENERAL_FAQS)
    for c in CATEGORIES:
        allf.extend(c["faqs"][:2])
    body = """
%s
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Sıkça Sorulan Sorular</p>
    <h1>Merak edilenler</h1>
    <p class="lead-p">Ürün seçimi, teslimat, montaj, garanti, taksit ve ticari soğutma hakkında en sık
    aldığımız soruların cevapları.</p>
  </div>
</section>
{{PERKS}}
%s
%s
""" % (crumbs(0, cb), faq_html(allf, "Tüm sorular"),
       cta_band(0, "Sorunuzun cevabı yoksa", "Mağazamızı arayın veya teklif formunu doldurun; aynı gün dönüş yapalım."))
    render("sikca-sorulan-sorular.html",
           "Sıkça Sorulan Sorular | Odabaşı Dayanıklı Tüketim",
           "Beyaz eşya seçimi, teslimat, montaj, garanti, taksit ve ticari soğutma hakkında sıkça sorulan sorular ve cevapları.",
           body, ld=[crumb_ld(cb), faq_ld(allf), local_business_ld()], active="sss", depth=0)
    register("sikca-sorulan-sorular.html", "0.6")

    # --- Iletisim ---
    cb = [("İletişim", None)]
    body = """
%s
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">İletişim</p>
    <h1>Fiyat teklifi ve bilgi</h1>
    <p class="lead-p">İhtiyacınızı yazın, uygun modelleri ve güncel fiyatları birlikte değerlendirelim.
    Teslimat ve montaj ücretsiz, taksit imkanı var. Toplu alım, ticari soğutma ve proje talepleri için de
    aynı formu kullanabilirsiniz.</p>
  </div>
</section>
{{PERKS}}
<section class="sec"><div class="wrap form-split">
  <div>
    <h2>Mağaza bilgileri</h2>
    <ul class="contact-list big">
      <li>%s<div><strong>Telefon</strong><a href="tel:%s">%s</a></div></li>
      <li>%s<div><strong>WhatsApp</strong><a href="https://wa.me/%s" target="_blank" rel="noopener">Mesaj gönderin</a></div></li>
      <li>%s<div><strong>Çalışma saatleri</strong><span>%s</span></div></li>
    </ul>
    <h2 style="margin-top:40px">Şubelerimiz</h2>
    <p class="muted">İzmir'de iki marka mağazamız var. İkisine de aynı numaradan ulaşabilirsiniz.</p>
    %s
    <h2 style="margin-top:40px">Hizmet bölgeleri</h2>
    <p class="muted">İzmir merkez ve ilçeleri, Aydın ve Manisa il ve ilçeleri.</p>
    <div class="chips">%s</div>
  </div>
  <div class="form-card">%s</div>
</div></section>
%s
""" % (crumbs(0, cb),
       icon("phone", "ico"), e(SITE["phone_tel"]), e(SITE["phone_display"]),
       icon("chat", "ico"), e(SITE["whatsapp"]),
       icon("check", "ico"), e(SITE["hours"]),
       branch_cards(0),
       "".join(loc_chip(0, l) for l in LOCATIONS),
       lead_form(0, "İletişim sayfası"),
       faq_html(GENERAL_FAQS[1:5], "İletişim ve teslimat hakkında"))
    render("iletisim.html",
           "İletişim ve Fiyat Teklifi | Odabaşı Dayanıklı Tüketim | İzmir",
           "Odabaşı Dayanıklı Tüketim iletişim bilgileri ve fiyat teklifi formu. İzmir, Aydın ve Manisa'da beyaz eşya, ankastre, klima ve ticari soğutma.",
           body, ld=[crumb_ld(cb), local_business_ld(),
                     {"@context": "https://schema.org", "@type": "ContactPage",
                      "url": url("iletisim.html"), "inLanguage": "tr-TR",
                      "mainEntity": {"@id": url("#store")}}] + branch_ld(),
           active="iletisim", depth=0)
    register("iletisim.html", "0.8")

    # --- 404 ---
    body = """
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">404</p>
    <h1>Aradığınız sayfa bulunamadı</h1>
    <p class="lead-p">Sayfa taşınmış veya adres yanlış yazılmış olabilir. Aşağıdan ürün gruplarımıza ulaşabilirsiniz.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="/index.html">Ana sayfaya dön</a></div>
  </div>
</section>
<section class="sec"><div class="wrap"><div class="grid cards">%s</div></div></section>
""" % "".join(cat_card(0, c) for c in CATEGORIES)
    render("404.html", "Sayfa bulunamadı | %s" % SITE["short"],
           "Aradığınız sayfa bulunamadı.", body, ld=[], depth=0)


# ---------------------------------------------------------------------------
# ASSET / SEO DOSYALARI
# ---------------------------------------------------------------------------
def build_assets():
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    with open(os.path.join(OUT, "assets", "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(OUT, "assets", "site.js"), "w", encoding="utf-8") as f:
        f.write(JS.replace("__WA__", SITE["whatsapp"]))
    here = os.path.dirname(os.path.abspath(__file__))
    for fn in ("logo.png", "logo-white.png", "turkiye-ege.svg"):
        src = os.path.join(here, "assets_src", fn)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(OUT, "assets", fn))
    mdir = os.path.join(OUT, "assets", "markalar")
    os.makedirs(mdir, exist_ok=True)
    found, missing = 0, []
    for b in BRANDS:
        f = brand_logo_file(b["slug"])
        if f:
            shutil.copyfile(os.path.join(BRAND_LOGO_DIR, f), os.path.join(mdir, f))
            found += 1
        else:
            missing.append(b["slug"])
    print("Marka logosu: %d/%d hazir" % (found, len(BRANDS)))
    if missing:
        print("  eksik (assets_src/markalar/ icine <slug>.svg olarak koyun):")
        print("  " + ", ".join(missing))
    with open(os.path.join(OUT, "assets", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
                '<rect width="64" height="64" rx="12" fill="#0B0C0F"/>'
                '<text x="32" y="45" font-family="Georgia,serif" font-size="38" font-weight="700" '
                'fill="#E60034" text-anchor="middle">O</text></svg>')


def build_seo_files():
    # robots.txt
    robots = """User-agent: *
Allow: /

# AI / arama motoru tarayicilari
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: CCBot
Allow: /

Sitemap: %s
""" % url("sitemap.xml")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    # sitemap.xml
    items = "".join(
        "  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>\n"
        % (url(p), SITE["updated"], fr, pr) for p, pr, fr in ALL_PAGES)
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % items)
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sm)

    # llms.txt  (GEO: AI motorlari icin yapisal ozet)
    cat_lines = "\n".join("- [%s](%s): %s" % (c["name"], url("kategori/%s.html" % c["slug"]), c["answer"].split(". ")[0] + ".")
                          for c in CATEGORIES)
    brand_lines = "\n".join("- [%s](%s)%s" % (b["name"], url("marka/%s.html" % b["slug"]),
                                              " - Yetkili bayi" if b["authorized"] else "")
                            for b in BRANDS)
    loc_lines = "\n".join("- [%s](%s)" % (l["name"], url("bolge/%s.html" % l["slug"])) for l in LOCATIONS)
    post_lines = "\n".join("- [%s](%s): %s" % (p["title"], url("blog/%s.html" % p["slug"]), p["desc"])
                           for p in POSTS)
    llms = """# %s

> İzmir merkezli beyaz eşya ve dayanıklı tüketim mağazası. LG, Uğur ve Altus yetkili bayisi.
> İzmir, Aydın ve Manisa'da beyaz eşya, ankastre mutfak ürünleri, klima ve ticari soğutma satışı,
> teslimat, montaj ve devreye alma hizmeti verir.

## Kurumsal bilgiler

- İşletme adı: %s
- Şubeler: LG Shop Çankaya (Konak/İzmir), Uğur Shop Eşrefpaşa (Konak/İzmir)
- Konum: %s
- Hizmet bölgeleri: İzmir (tüm ilçeler), Aydın, Manisa
- Telefon: %s
- E-posta: %s
- Çalışma saatleri: %s
- Yetkili bayilik: LG, Uğur, Altus
- Diğer satılan markalar: Hoover, TCL, Electrolux, Şenocak, Grundig, Kärcher, Rota

## Ürün grupları

%s

## Markalar

%s

## Hizmet bölgeleri

%s

## Rehber içerikleri

%s

## Kurumsal sayfalar

- [Hakkımızda](%s)
- [Servis ve Destek](%s)
- [Sıkça Sorulan Sorular](%s)
- [İletişim](%s)

Son güncelleme: %s
""" % (SITE["name"], SITE["name"], SITE["address_line"],
       SITE["phone_display"], SITE["email"], SITE["hours"],
       cat_lines, brand_lines, loc_lines, post_lines,
       url("hakkimizda.html"), url("servis-ve-destek.html"),
       url("sikca-sorulan-sorular.html"), url("iletisim.html"), SITE["updated"])
    with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(llms)

    # .htaccess (Apache/cPanel icin temel yonlendirme ve cache)
    with open(os.path.join(OUT, ".htaccess"), "w", encoding="utf-8") as f:
        f.write("""ErrorDocument 404 /404.html
Options -Indexes

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript text/xml application/xml image/svg+xml
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType text/html "access plus 1 hour"
</IfModule>

<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
""")


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
HERO_ART = """
<svg class="art" viewBox="0 0 780 500" role="img" aria-label="Buzdolabi, camasir makinesi, ankastre firin, bulasik makinesi, klima ve televizyon cizimi">
  <title>Beyaz eşya ürün grubu çizimi</title>
  <defs>
    <filter id="ng" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <linearGradient id="scr" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1A1D24"/><stop offset="55%" stop-color="#2A2F3A"/>
      <stop offset="100%" stop-color="#12141A"/>
    </linearGradient>
    <radialGradient id="halo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#E60034" stop-opacity=".16"/>
      <stop offset="100%" stop-color="#E60034" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <ellipse cx="400" cy="300" rx="360" ry="230" fill="url(#halo)"/>
  <g fill="#101216" opacity=".07">
    <ellipse cx="116" cy="436" rx="76" ry="7"/>
    <ellipse cx="274" cy="436" rx="76" ry="7"/>
    <ellipse cx="434" cy="436" rx="76" ry="7"/>
    <ellipse cx="594" cy="436" rx="76" ry="7"/>
  </g>

  <!-- neon zemin ve duvar cizgileri -->
  <g filter="url(#ng)" stroke="#E60034" stroke-linecap="round" fill="none">
    <path d="M30 432 H750" stroke-width="3"/>
    <path d="M596 62 H744" stroke-width="2.5" opacity=".75"/>
    <path d="M648 44 H744" stroke-width="2.5" opacity=".45"/>
  </g>

  <g fill="#FFFFFF" stroke="#14171D" stroke-width="2.4" stroke-linejoin="round">

    <!-- klima ic unite -->
    <rect x="210" y="96" width="176" height="52" rx="11"/>
    <path d="M222 132 H374" stroke-width="2"/>
    <path d="M222 120 H374" stroke-width="2" opacity=".5"/>
    <!-- akilli sinyal -->
    <g fill="none" stroke="#E60034" stroke-width="2.6" stroke-linecap="round" filter="url(#ng)">
      <path d="M392 84a20 20 0 0 1 22 0"/>
      <path d="M397 93a12 12 0 0 1 12 0"/>
      <circle cx="403" cy="101" r="2.2" fill="#E60034"/>
    </g>

    <!-- televizyon -->
    <rect x="430" y="100" width="252" height="152" rx="9"/>
    <rect x="441" y="111" width="230" height="130" rx="5" fill="url(#scr)" stroke="none"/>
    <path d="M556 252 v20 M528 274 H584" stroke-width="2.6" stroke-linecap="round"/>
    <g filter="url(#ng)"><path d="M452 232 H560" stroke="#E60034" stroke-width="2.6" stroke-linecap="round" fill="none"/></g>

    <!-- buzdolabi -->
    <rect x="50" y="120" width="132" height="312" rx="12"/>
    <path d="M50 226 H182" stroke-width="2.4"/>
    <rect x="68" y="142" width="48" height="28" rx="6" fill="none" stroke="#E60034" stroke-width="2.2"/>
    <path d="M78 156 H106" stroke="#E60034" stroke-width="2" stroke-linecap="round"/>
    <g filter="url(#ng)" stroke="#E60034" stroke-width="6" stroke-linecap="round" fill="none">
      <path d="M166 182 V212"/>
      <path d="M166 246 V296"/>
    </g>
    <path d="M68 262 H150 M68 296 H150 M68 330 H150" stroke-width="1.8" opacity=".35"/>

    <!-- camasir makinesi -->
    <rect x="206" y="266" width="136" height="166" rx="11"/>
    <path d="M206 300 H342" stroke-width="2.2"/>
    <circle cx="274" cy="372" r="47"/>
    <g filter="url(#ng)"><circle cx="274" cy="372" r="33" fill="none" stroke="#E60034" stroke-width="3"/></g>
    <circle cx="226" cy="283" r="3.4" fill="#14171D" stroke="none"/>
    <circle cx="240" cy="283" r="3.4" fill="#14171D" stroke="none"/>
    <circle cx="254" cy="283" r="3.4" fill="#14171D" stroke="none"/>
    <circle cx="322" cy="283" r="10" fill="none" stroke="#E60034" stroke-width="2.4"/>

    <!-- ankastre firin -->
    <rect x="366" y="266" width="136" height="166" rx="11"/>
    <path d="M366 302 H502" stroke-width="2.2"/>
    <rect x="382" y="322" width="104" height="92" rx="7" fill="#F3F5F8"/>
    <rect x="392" y="332" width="84" height="72" rx="5" fill="none" stroke="#E60034" stroke-width="1.8" opacity=".5"/>
    <g filter="url(#ng)"><path d="M382 310 H486" stroke="#E60034" stroke-width="5" stroke-linecap="round" fill="none"/></g>
    <circle cx="382" cy="285" r="6"/><circle cx="402" cy="285" r="6"/><circle cx="422" cy="285" r="6"/>
    <path d="M402 344 a22 22 0 0 1 44 0 a22 22 0 0 1 -44 0" stroke-width="1.8" opacity=".4" fill="none"/>

    <!-- bulasik makinesi -->
    <rect x="526" y="266" width="136" height="166" rx="11"/>
    <path d="M526 302 H662" stroke-width="2.2"/>
    <g filter="url(#ng)"><path d="M540 284 H612" stroke="#E60034" stroke-width="5" stroke-linecap="round" fill="none"/></g>
    <rect x="628" y="278" width="22" height="9" rx="3" fill="#E60034" stroke="none"/>
    <path d="M546 322 H642 M546 356 H642 M546 390 H642" stroke-width="1.8" opacity=".3"/>
  </g>
</svg>
"""

CSS = r"""
:root{
  --brand:#E60034; --brand-2:#B70328; --brand-soft:#FFF1F4; --brand-line:#FBD3DC;
  --ink:#101216; --ink-2:#232830; --ink-3:#454C58;
  --muted:#6B7280; --muted-2:#9AA3AF;
  --line:#E5E8EC; --line-2:#F1F3F6;
  --bg:#FFFFFF; --soft:#F7F9FB; --dark:#0B0C0F; --dark-2:#15171C;
  --ok:#1F7A4D;
  --r:14px; --r-sm:10px;
  --shadow:0 1px 2px rgba(16,18,22,.05), 0 8px 26px rgba(16,18,22,.07);
  --shadow-lg:0 2px 6px rgba(16,18,22,.06), 0 24px 56px rgba(16,18,22,.11);
  --glow:0 0 0 1px rgba(230,0,52,.18), 0 8px 26px rgba(230,0,52,.16);
  --w:1200px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
  font-size:16px; line-height:1.65; -webkit-font-smoothing:antialiased;
}
h1,h2,h3,h4{font-family:Manrope,Inter,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; line-height:1.18; letter-spacing:-.025em; margin:0 0 .5em}
h1{font-size:clamp(2rem,4.2vw,3.35rem); font-weight:800}
h2{font-size:clamp(1.45rem,2.5vw,2.15rem); font-weight:800}
h3{font-size:1.08rem; font-weight:700}
p{margin:0 0 1em}
a{color:var(--brand-2); text-decoration:none}
a:hover{text-decoration:underline}
img,svg{max-width:100%}
.wrap{width:100%; max-width:var(--w); margin:0 auto; padding-inline:20px}
.skip{position:absolute; left:-9999px}
.skip:focus{left:12px; top:12px; z-index:99; background:#fff; padding:10px 16px; border-radius:8px}
.ico{width:20px;height:20px;flex:none}
.ico.sm{width:16px;height:16px}
.ico.lg{width:26px;height:26px}
.muted{color:var(--muted)}

/* ---- topbar / header ---- */
.topbar{background:var(--dark); color:#D5D9E0; font-size:.8rem}
.topbar-in{display:flex; gap:22px; padding:9px 20px; align-items:center}
.topbar-in span{display:flex; align-items:center; gap:6px; white-space:nowrap}
.topbar-in .ico{color:var(--brand)}
.topbar-r{margin-left:auto; color:#9AA3AF}
.hd{position:sticky; top:0; z-index:50; background:#fff; border-bottom:1px solid var(--line)}
.hd-in{display:flex; align-items:center; gap:22px; padding-block:13px}
.logo{display:block; flex:none; line-height:0}
.logo:hover{text-decoration:none}
.logo img{height:42px; width:auto; display:block}
.ft .logo img{height:46px}
.nav{display:flex; align-items:center; gap:2px; margin-left:auto}
.nav-link{display:inline-flex;align-items:center;gap:4px;padding:9px 12px;border-radius:8px;font-size:.92rem;font-weight:500;color:var(--ink-2);background:none;border:0;cursor:pointer;font-family:inherit}
.nav-link:hover{background:var(--soft); text-decoration:none; color:var(--brand)}
.nav-link.is-active{color:var(--brand)}
.chev{width:14px;height:14px;transition:transform .18s}
.has-menu{position:relative}
.has-menu.open .chev{transform:rotate(180deg)}
.mega{position:absolute; top:calc(100% + 10px); left:0; background:#fff; border:1px solid var(--line); border-radius:var(--r); box-shadow:var(--shadow-lg); padding:10px; display:none; z-index:60}
.has-menu.open .mega{display:grid}
.mega a{display:flex;align-items:center;gap:8px;padding:9px 12px;border-radius:var(--r-sm);color:var(--ink-2);font-size:.9rem;white-space:nowrap}
.mega a:hover{background:var(--brand-soft); text-decoration:none; color:var(--brand-2)}
.mega-cats{grid-template-columns:1fr 1fr; width:520px}
.mega-brands{grid-template-columns:1fr 1fr; width:440px}
.mega-locs{grid-template-columns:1fr 1fr; width:400px}
.tag{font-size:.62rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;background:var(--brand-soft);color:var(--brand-2);padding:2px 6px;border-radius:5px;margin-left:auto}
.hd-cta{display:flex;align-items:center;gap:10px;flex:none}
.burger{display:none;width:42px;height:40px;border:1px solid var(--line);border-radius:10px;background:#fff;cursor:pointer;flex-direction:column;justify-content:center;align-items:center;gap:4px}
.burger span{display:block;width:18px;height:2px;background:var(--ink);border-radius:2px;transition:.2s}
.burger[aria-expanded="true"] span:nth-child(1){transform:translateY(6px) rotate(45deg)}
.burger[aria-expanded="true"] span:nth-child(2){opacity:0}
.burger[aria-expanded="true"] span:nth-child(3){transform:translateY(-6px) rotate(-45deg)}

/* ---- buttons ---- */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:11px 18px;border-radius:10px;font-weight:600;font-size:.92rem;border:1px solid transparent;cursor:pointer;transition:.16s;font-family:inherit;text-decoration:none}
.btn:hover{text-decoration:none;transform:translateY(-1px)}
.btn-lg{padding:14px 26px;font-size:1rem}
.btn-primary{background:var(--brand);color:#fff;box-shadow:0 6px 20px rgba(230,0,52,.25)}
.btn-primary:hover{background:var(--brand-2);color:#fff;box-shadow:0 10px 26px rgba(230,0,52,.32)}
.btn-outline{background:#fff;color:var(--ink);border-color:var(--line)}
.btn-outline:hover{border-color:var(--brand);color:var(--brand)}
.btn-ghost{background:var(--soft);color:var(--ink)}
.btn-ghost:hover{background:var(--brand-soft);color:var(--brand-2)}

/* ---- hero ---- */
.hero{position:relative;overflow:hidden;background:linear-gradient(180deg,#FFFFFF 0%,#F7F9FC 100%);border-bottom:1px solid var(--line)}
.hero::before{content:"";position:absolute;inset:0;background:radial-gradient(760px 400px at 78% 22%, rgba(230,0,52,.10), transparent 66%);pointer-events:none}
.hero-in{display:grid;grid-template-columns:1.02fr 1.08fr;gap:48px;align-items:center;padding-block:70px 76px;position:relative;z-index:1}
.eyebrow{display:inline-flex;align-items:center;gap:7px;font-size:.76rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--brand);margin:0 0 14px}
.hero h1{max-width:15ch}
.hero h1 em{font-style:normal;color:var(--brand);position:relative;white-space:nowrap}
.hero h1 em::after{content:"";position:absolute;left:0;right:0;bottom:.06em;height:5px;border-radius:4px;background:var(--brand);opacity:.22}
.lead-p{font-size:1.06rem;color:var(--ink-3)}
.hero .lead-p{max-width:52ch}
.hero-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.hero-points{list-style:none;margin:30px 0 0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:10px 22px}
.hero-points li{display:flex;align-items:center;gap:8px;font-size:.92rem;font-weight:500;color:var(--ink-2)}
.hero-points .ico{color:var(--brand)}
.hero-art{position:relative}
.hero-art .art{width:100%;height:auto;display:block}

.page-hero{background:linear-gradient(180deg,#FFFFFF,#F7F9FC);border-bottom:1px solid var(--line);padding-block:52px 46px;position:relative}
.page-hero::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:3px;background:linear-gradient(90deg,var(--brand),rgba(230,0,52,0) 62%)}
.page-hero .lead-p{max-width:70ch}
.page-hero .hero-actions{margin-top:20px}
.badge{display:inline-block;vertical-align:middle;margin-left:12px;font-size:.62rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;background:var(--brand);color:#fff;padding:5px 10px;border-radius:6px;position:relative;top:-6px}
.badge-alt{background:var(--ink)}

/* ---- perks ---- */
.perks{background:#fff;border-bottom:1px solid var(--line)}
.perks-in{display:grid;grid-template-columns:repeat(4,1fr);gap:0;padding-block:0}
.perk{display:flex;gap:14px;align-items:flex-start;padding:26px 24px;border-right:1px solid var(--line-2)}
.perk:first-child{padding-left:0}
.perk:last-child{border-right:0;padding-right:0}
.perk .ico{color:var(--brand);margin-top:2px}
.perk strong{display:block;font-family:Manrope,Inter,"Segoe UI",Roboto,Arial,sans-serif;font-weight:700;font-size:.98rem;color:var(--ink)}
.perk span{display:block;font-size:.83rem;color:var(--muted);line-height:1.5;margin-top:3px}
.perks-compact .perk{padding-block:18px}
.perks-compact .perk strong{font-size:.9rem}

/* ---- ask (LG/Ugur) ---- */
.ask{background:var(--dark);color:#E6E9EE;position:relative;overflow:hidden}
.ask::before{content:"";position:absolute;inset:0;background:radial-gradient(620px 320px at 82% 0%, rgba(230,0,52,.30), transparent 64%)}
.ask::after{content:"";position:absolute;left:0;top:0;width:100%;height:3px;background:linear-gradient(90deg,var(--brand),rgba(230,0,52,0) 55%)}
.ask-in{position:relative;z-index:1;display:grid;grid-template-columns:1.5fr .8fr;gap:48px;align-items:center;padding-block:62px}
.ask h2{color:#fff;max-width:20ch}
.ask p{color:#B7BFCA;max-width:62ch}
.ask-list{list-style:none;padding:0;margin:22px 0 0;display:flex;flex-direction:column;gap:10px}
.ask-list li{display:flex;align-items:flex-start;gap:10px;font-size:.95rem;color:#D6DCE4}
.ask-list .ico{color:var(--brand);margin-top:4px}
.ask .btn-outline{background:transparent;color:#fff;border-color:rgba(255,255,255,.28)}
.ask .btn-outline:hover{border-color:var(--brand);color:#fff;background:rgba(230,0,52,.12)}
.ask-brands{display:grid;gap:14px}
.ask-brand{display:flex;flex-direction:column;align-items:center;gap:10px;padding:18px;border:1px solid rgba(255,255,255,.16);border-radius:var(--r);background:rgba(255,255,255,.04);color:#fff;transition:.18s}
.ask-brand:hover{text-decoration:none;color:#fff;border-color:var(--brand);background:rgba(230,0,52,.1);transform:translateY(-2px)}
.ask-brand strong{font-family:Manrope,Inter,"Segoe UI",Roboto,Arial,sans-serif;font-size:1.9rem;font-weight:800;line-height:1}
.ask-brand .bmark{justify-content:center;background:#fff;border-radius:11px;padding:16px 20px;width:100%}
.ask-brand .bmark img{width:132px}
.ask-brand .bmark-word{color:var(--ink)}
.ask-brand > span{font-size:.7rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--brand)}

/* ---- crumbs ---- */
.crumbs{background:#fff;border-bottom:1px solid var(--line-2);font-size:.82rem;color:var(--muted)}
.crumbs .wrap{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding-block:11px}
.crumbs a{color:var(--muted)}
.crumbs a:hover{color:var(--brand)}
.crumbs .sep{color:var(--line)}
.crumbs span[aria-current]{color:var(--ink);font-weight:500}

/* ---- sections ---- */
.sec{padding-block:64px}
.sec-soft{background:var(--soft)}
.sec-dark{background:var(--soft);border-block:1px solid var(--line)}
.sec-head{max-width:62ch;margin-bottom:32px}
.sec-head h2{position:relative;padding-top:16px}
.sec-head h2::before{content:"";position:absolute;top:0;left:0;width:44px;height:3px;border-radius:3px;background:var(--brand);box-shadow:0 0 12px rgba(230,0,52,.55)}
.sec-head p{color:var(--muted);margin:0}
.grid{display:grid;gap:16px}
.cards{grid-template-columns:repeat(3,1fr)}
.feats{grid-template-columns:repeat(4,1fr)}
.posts{grid-template-columns:repeat(3,1fr)}
.lines{grid-template-columns:repeat(3,1fr)}
.more{margin-top:26px}
.more a{display:inline-flex;align-items:center;gap:7px;font-weight:600;color:var(--brand-2)}

/* ---- cards ---- */
.card{display:flex;align-items:center;gap:14px;background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px;color:var(--ink);transition:.16s}
.card:hover{text-decoration:none;border-color:var(--brand);box-shadow:var(--glow);transform:translateY(-2px)}
.card-ico{width:46px;height:46px;flex:none;border-radius:11px;background:var(--brand-soft);color:var(--brand);display:grid;place-items:center}
.card-body{display:flex;flex-direction:column;min-width:0}
.card-body strong{font-family:Manrope,Inter,"Segoe UI",Roboto,Arial,sans-serif;font-weight:700;font-size:1rem}
.card-body span{font-size:.79rem;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.card-go{margin-left:auto;color:var(--muted-2);flex:none}
.card:hover .card-go{color:var(--brand)}

.feat{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:26px 24px;position:relative;overflow:hidden}
.feat::before{content:"";position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,var(--brand),rgba(230,0,52,0))}
.feat .ico{color:var(--brand);margin-bottom:14px}
.feat h3{margin-bottom:8px}
.feat p{margin:0;font-size:.9rem;color:var(--muted)}

.line{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:20px;border-left:3px solid var(--brand)}
.line strong{display:block;font-family:Manrope,Inter,"Segoe UI",Roboto,Arial,sans-serif;font-size:1rem;margin-bottom:6px}
.line p{margin:0;font-size:.88rem;color:var(--muted)}

.chips{display:flex;flex-wrap:wrap;gap:10px}
.chip{display:inline-flex;align-items:center;gap:8px;background:#fff;border:1px solid var(--line);border-radius:999px;padding:9px 16px;color:var(--ink);font-size:.9rem;font-weight:500;transition:.16s}
.chip:hover{text-decoration:none;border-color:var(--brand);color:var(--brand);box-shadow:var(--glow)}
.chip .tag{margin-left:2px}
.chip .ico{color:var(--muted-2)}
.chip:hover .ico{color:var(--brand)}

.post-card{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:24px;color:var(--ink);transition:.16s}
.post-card:hover{text-decoration:none;border-color:var(--brand);box-shadow:var(--glow);transform:translateY(-2px)}
.post-cat{font-size:.68rem;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--brand);margin-bottom:10px}
.post-card h3{font-size:1.05rem;margin-bottom:8px}
.post-card p{font-size:.87rem;color:var(--muted);margin-bottom:14px}
.post-date{margin-top:auto;font-size:.78rem;color:var(--muted-2)}

/* ---- hizmet haritasi ---- */
.smap{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:44px;align-items:start}
.smap-fig{position:relative;margin:0;background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:16px 16px 12px;box-shadow:var(--shadow)}
.smap-fig svg{width:100%;height:auto;display:block;border-radius:8px;overflow:hidden}
.smap-fig figcaption{margin-top:12px;padding-top:12px;border-top:1px solid var(--line-2);font-size:.75rem;color:var(--muted);line-height:1.5}
.smap-inset{position:absolute;right:24px;bottom:70px;width:118px;height:auto;
  background:rgba(255,255,255,.94);border:1px solid var(--line);border-radius:7px;padding:5px 7px;
  box-shadow:0 2px 10px rgba(16,18,22,.08)}
.smap-water{fill:#D5E7F1}
.smap-land{fill:#F0F2F5;stroke:#fff;stroke-width:.9}
.smap-prov-area{fill:var(--tint);fill-opacity:.16;stroke:var(--tint);stroke-opacity:.7;stroke-width:1.1}
.smap-prov{font:800 6px/1 Manrope,Inter,"Segoe UI",Roboto,Arial,sans-serif;letter-spacing:.12em;
  text-anchor:middle;opacity:.85;paint-order:stroke;stroke:#fff;stroke-width:2.4;stroke-linejoin:round}
.smap-dot{fill:#fff;stroke:var(--ink-2);stroke-width:1;transition:.18s;cursor:pointer;
  paint-order:stroke;vector-effect:non-scaling-stroke}
.smap-dot.is-hub{fill:var(--ink);stroke:#fff;stroke-width:1.4}
.smap-hit:hover .smap-dot,.smap-hit.is-hi .smap-dot{fill:var(--brand);stroke:#fff;stroke-width:1.4;r:4.4}
.smap-dot.is-active{fill:var(--brand);stroke:#fff;stroke-width:1.4}
.smap-hit:focus-visible{outline:2px solid var(--brand);outline-offset:1px}
.smap-store circle{fill:var(--brand)}
.smap-store .smap-pulse{fill:var(--brand);opacity:.18}
.smap-store .smap-core{fill:#fff}
.smap-scale path{stroke:var(--ink-3);stroke-width:.8;fill:none;opacity:.7}
.smap-scale text{font:600 4.6px Inter,sans-serif;fill:var(--ink-3);text-anchor:middle;letter-spacing:.05em;opacity:.85}
.smap-north path{fill:var(--ink-3);opacity:.7}
.smap-north text{font:700 4.6px Manrope,Inter,sans-serif;fill:var(--ink-3);text-anchor:middle;opacity:.85}
.smap-legend{display:flex;flex-wrap:wrap;gap:8px 20px;padding-bottom:20px;margin-bottom:6px;border-bottom:1px solid var(--line)}
.smap-legend span{display:inline-flex;align-items:center;gap:8px;font-size:.83rem;color:var(--ink-3)}
.smap-legend i{width:13px;height:13px;border-radius:50%;flex:none}
.smap-legend .lg-store{background:var(--brand);box-shadow:0 0 0 4px rgba(230,0,52,.16)}
.smap-legend .lg-hub{background:var(--ink)}
.smap-legend .lg-dot{background:#fff;border:2px solid var(--ink-3)}
.smap-group{padding-block:18px;border-bottom:1px solid var(--line)}
.smap-group h3{display:flex;align-items:center;gap:9px;font-size:.82rem;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);margin-bottom:12px}
.smap-key{width:11px;height:11px;border-radius:3px;display:inline-block;opacity:.85}
.smap-group ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:7px}
.smap-group li a,.smap-group li span{display:inline-block;padding:6px 12px;border-radius:999px;font-size:.85rem;line-height:1.3}
.smap-group li a{background:#fff;border:1px solid var(--line);color:var(--ink-2)}
.smap-group li a:hover,.smap-group li a.is-hi{text-decoration:none;border-color:var(--brand);color:var(--brand);box-shadow:var(--glow)}
.smap-group li a.is-active{background:var(--brand);border-color:var(--brand);color:#fff}
.smap-group li span{color:var(--muted);border:1px solid transparent}
.smap-side .btn{margin-top:22px}
@media (max-width:900px){.smap{grid-template-columns:1fr;gap:28px}.smap-fig{max-width:520px;margin-inline:auto}}
@media (max-width:520px){.smap-inset{width:96px;right:20px;bottom:66px}}
@media (prefers-reduced-motion:reduce){.smap-dot{transition:none}}

/* ---- subeler ---- */
.branches{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:0 0 1em}
.branch{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:22px;border-top:3px solid var(--brand)}
.br-head{display:flex;align-items:center;gap:14px;margin-bottom:12px}
.br-head > div{min-width:0}
.form-split .branches,.smap-side .branches{grid-template-columns:1fr}
.br-head .bmark{background:var(--soft);border:1px solid var(--line-2);border-radius:9px;padding:9px 12px;flex:none}
.br-head strong{display:block;font-family:Manrope,Inter,"Segoe UI",Roboto,Arial,sans-serif;font-size:1.02rem;line-height:1.25}
.br-head span{display:block;font-size:.82rem;color:var(--muted);margin-top:2px}
.branch p{font-size:.88rem;color:var(--muted);margin:0 0 14px}
.br-links{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center}
.br-links a{display:inline-flex;align-items:center;gap:6px;font-size:.86rem;font-weight:600}
.br-tel{color:var(--brand-2)}
.br-map,.br-brand{color:var(--ink-3)}
.br-map:hover,.br-brand:hover{color:var(--brand)}
.branches-compact{grid-template-columns:1fr;gap:12px;margin-top:20px}
.branches-compact .branch{padding:16px 18px;border-top-width:2px}
.branches-compact .br-head{margin-bottom:0}
.branches-compact .br-links{margin-top:12px}
.ft-addr .ft-br{display:block;line-height:1.45}
.ft-addr .ft-br b{display:block;color:#fff;font-weight:600}
.bmark-sm img{width:66px}
.bmark-sm .bmark-word{font-size:1rem}

/* ---- marka logolari ---- */
.bmark{display:inline-flex;align-items:center;justify-content:center;line-height:1}
.bmark img{width:150px;height:auto;display:block}
.bmark-word{font-family:Manrope,Inter,"Segoe UI",Roboto,Arial,sans-serif;font-weight:800;font-size:1.28rem;letter-spacing:-.03em;color:var(--ink);white-space:nowrap}
.bmark-lg img{width:190px}
.bmark-lg .bmark-word{font-size:1.75rem}
.bmark-xl img{width:240px}
.bmark-xl .bmark-word{font-size:2.3rem}
.bmark-inv .bmark-word{color:#fff}
.bmark-inv img{filter:brightness(0) invert(1)}

.bwall{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
.bwall-item{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;
  min-height:122px;padding:26px 14px 22px;background:#fff;border:1px solid var(--line);border-radius:var(--r);
  color:var(--ink);text-align:center;transition:.16s;position:relative;overflow:hidden}
.bwall-item:hover{text-decoration:none;border-color:var(--brand);box-shadow:var(--glow);transform:translateY(-2px)}
.bwall-item.is-auth{border-color:var(--brand-line)}
.bwall-item .bmark{min-height:48px;align-items:center}
.bwall-item .bmark img{width:146px;filter:grayscale(1) contrast(.85);opacity:.55;transition:.2s}
.bwall-item:hover .bmark img{filter:none;opacity:1}
.bwall-item .bmark-word{color:#9B9B9B;font-weight:700;transition:.18s}
.bwall-item:hover .bmark-word{color:var(--ink)}
.bwall-name{font-size:.8rem;font-weight:600;color:var(--muted);letter-spacing:.02em}
.bwall-item .bwall-name{display:none}
.bwall-item.is-nologo .bwall-name{display:none}
.bwall-item.is-nologo .bmark-word{font-size:1.4rem}
.bwall-tag{position:absolute;top:0;right:0;font-size:.58rem;font-weight:800;letter-spacing:.07em;
  text-transform:uppercase;background:var(--muted-2);color:#fff;padding:4px 9px;border-bottom-left-radius:9px;transition:.18s}
.bwall-item:hover .bwall-tag{background:var(--brand)}
.sec-soft .bwall-item{background:#fff}

.brand-head{display:flex;align-items:center;gap:24px;flex-wrap:wrap;margin-bottom:.5em}
.brand-head h1{margin:0}
.brand-head .bmark{padding:14px 20px;background:#fff;border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow)}

/* ---- answer box (GEO) ---- */
.answer{background:var(--brand-soft);border:1px solid var(--brand-line);border-left:4px solid var(--brand);border-radius:var(--r-sm);padding:20px 22px;margin:0 0 36px}
.answer-label{display:block;font-size:.7rem;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--brand-2);margin-bottom:8px}
.answer p{margin:0;font-size:1.02rem;line-height:1.6;color:var(--ink-2)}
.sec > .wrap > .answer:only-child{margin-bottom:0}

/* ---- prose ---- */
.prose{max-width:840px}
.prose-sec{margin-bottom:40px}
.prose-sec h2{margin-bottom:14px}
.prose p{color:var(--ink-3)}
.ticks,.areas{list-style:none;padding:0;margin:0 0 1em}
.ticks li{position:relative;padding-left:26px;margin-bottom:10px;color:var(--ink-3)}
.ticks li::before{content:"";position:absolute;left:0;top:.52em;width:9px;height:9px;border-radius:3px;background:var(--brand)}
.areas{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.areas li{background:var(--soft);border:1px solid var(--line-2);border-radius:8px;padding:8px 12px;font-size:.87rem;color:var(--ink-2)}
.steps{margin:0;padding-left:0;list-style:none;counter-reset:s}
.steps li{counter-increment:s;position:relative;padding-left:44px;margin-bottom:16px;color:var(--ink-3)}
.steps li::before{content:counter(s);position:absolute;left:0;top:0;width:30px;height:30px;border-radius:9px;background:var(--brand);color:#fff;display:grid;place-items:center;font-family:Manrope,Inter,"Segoe UI",Roboto,Arial,sans-serif;font-weight:800;font-size:.85rem}
.toc{background:var(--soft);border:1px solid var(--line-2);border-radius:var(--r);padding:22px 26px;margin-bottom:40px}
.toc h2{font-size:.9rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:12px;padding-top:0}
.toc h2::before{display:none}
.toc ol{margin:0;padding-left:20px}
.toc li{margin-bottom:6px}
.toc a{color:var(--ink-2)}

/* ---- table ---- */
.table-wrap{overflow-x:auto;margin:0 0 40px;border:1px solid var(--line);border-radius:var(--r)}
table{width:100%;border-collapse:collapse;font-size:.9rem;min-width:520px}
caption{text-align:left;padding:16px 18px;font-weight:700;font-family:Manrope,Inter,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);border-bottom:2px solid var(--brand)}
th{text-align:left;padding:12px 18px;background:var(--soft);font-weight:600;color:var(--ink-2);font-size:.82rem;border-bottom:1px solid var(--line)}
td{padding:12px 18px;border-bottom:1px solid var(--line-2);color:var(--ink-3)}
tbody tr:last-child td{border-bottom:0}

/* ---- faq ---- */
.faq{background:var(--soft)}
.faq .wrap{max-width:900px}
.faq h2{margin-bottom:24px}
.faq-list{display:flex;flex-direction:column;gap:10px}
.faq-item{background:#fff;border:1px solid var(--line);border-radius:var(--r-sm);overflow:hidden}
.faq-item[open]{border-color:var(--brand-line)}
.faq-item summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:18px 20px;font-weight:700;font-family:Manrope,Inter,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);font-size:1rem}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary:hover{color:var(--brand)}
.plus{width:18px;height:18px;flex:none;stroke:var(--muted-2);stroke-width:2;fill:none;stroke-linecap:round;transition:transform .2s}
.faq-item[open] .plus{transform:rotate(45deg);stroke:var(--brand)}
.faq-a{padding:0 20px 20px}
.faq-a p{margin:0;color:var(--ink-3);font-size:.94rem}

/* ---- band ---- */
.band{background:var(--brand-soft);border-block:1px solid var(--brand-line)}
.band-in{display:flex;align-items:center;justify-content:space-between;gap:32px;padding-block:40px;flex-wrap:wrap}
.band h2{margin-bottom:6px;font-size:1.45rem;padding-top:0}
.band h2::before{display:none}
.band p{margin:0;color:var(--ink-3);max-width:56ch}
.band-actions{display:flex;gap:12px;flex-wrap:wrap}

/* ---- form ---- */
.form-split{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start}
.form-card{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:28px;box-shadow:var(--shadow);border-top:3px solid var(--brand)}
.lead label{display:block;font-size:.82rem;font-weight:600;color:var(--ink-2);margin-bottom:14px}
.lead-row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.lead input,.lead select,.lead textarea{width:100%;margin-top:6px;padding:11px 13px;border:1px solid var(--line);border-radius:9px;font-family:inherit;font-size:.92rem;color:var(--ink);background:#fff;font-weight:400}
.lead input:focus,.lead select:focus,.lead textarea:focus{outline:2px solid var(--brand);outline-offset:1px;border-color:transparent}
.lead textarea{resize:vertical}
.lead .btn{width:100%;margin-top:6px}
.lead-note{font-size:.78rem;color:var(--muted);margin:14px 0 0}
.contact-list{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:14px}
.contact-list li{display:flex;align-items:center;gap:12px;color:var(--ink-3)}
.contact-list .ico{color:var(--brand);flex:none}
.contact-list.big li{align-items:flex-start;gap:14px;padding-bottom:14px;border-bottom:1px solid var(--line-2)}
.contact-list.big strong{display:block;font-family:Manrope,Inter,"Segoe UI",Roboto,Arial,sans-serif;font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:2px}
.contact-list.big a,.contact-list.big span{font-size:1rem;color:var(--ink)}
.article-head{max-width:840px;padding-block:52px 8px}
.article .meta{color:var(--muted);font-size:.86rem}

/* ---- footer ---- */
.ft{background:var(--dark);color:#9AA3AF;padding-block:56px 0;position:relative}
.ft::before{content:"";position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,var(--brand),rgba(230,0,52,0) 48%)}
.ft-in{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr 1fr;gap:36px}
.ft .logo{margin-bottom:18px}
.ft-desc{font-size:.86rem;line-height:1.6;max-width:40ch}
.ft-addr{font-style:normal;display:flex;flex-direction:column;gap:5px;font-size:.86rem;margin-top:16px}
.ft-addr a{color:#fff}
.ft-col h3{color:#fff;font-size:.8rem;text-transform:uppercase;letter-spacing:.08em;margin-bottom:14px}
.ft-col ul{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px}
.ft-col a{color:#9AA3AF;font-size:.87rem}
.ft-col a:hover{color:var(--brand)}
.ft-bot{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-top:44px;padding-block:20px;border-top:1px solid rgba(255,255,255,.09);font-size:.8rem;color:#6B7280}

/* ---- whatsapp float ---- */
.wa{position:fixed;right:18px;bottom:18px;z-index:80;display:inline-flex;align-items:center;gap:8px;background:var(--ok);color:#fff;padding:12px 18px;border-radius:999px;font-weight:600;font-size:.9rem;box-shadow:0 6px 22px rgba(31,122,77,.35)}
.wa:hover{text-decoration:none;color:#fff;background:#186339}

/* ---- responsive ---- */
@media (max-width:1080px){
  .cards,.posts,.lines{grid-template-columns:repeat(2,1fr)}
  .feats{grid-template-columns:repeat(2,1fr)}
  .bwall{grid-template-columns:repeat(4,1fr)}
  .ft-in{grid-template-columns:1fr 1fr 1fr}
  .hero-in{grid-template-columns:1fr;gap:36px}
  .hero h1{max-width:20ch}
  .ask-in{grid-template-columns:1fr;gap:32px}
  .ask-brands{grid-template-columns:1fr 1fr}
  .perks-in{grid-template-columns:1fr 1fr}
  .perk{border-right:0;border-bottom:1px solid var(--line-2);padding-inline:0 24px}
}
@media (max-width:900px){
  html,body{overflow-x:clip}
  .nav{visibility:hidden;position:fixed;top:0;right:0;bottom:0;width:min(340px,86vw);background:#fff;flex-direction:column;align-items:stretch;gap:2px;padding:96px 18px 40px;box-shadow:-12px 0 40px rgba(16,18,22,.16);transform:translateX(100%);transition:transform .24s;overflow-y:auto;z-index:70}
  .nav.open{transform:translateX(0);visibility:visible}
  .burger{display:flex;z-index:75}
  .hd-cta .btn-ghost{display:none}
  .has-menu{position:static}
  .mega{position:static;width:auto!important;box-shadow:none;border:0;border-radius:0;padding:0 0 8px 12px;grid-template-columns:1fr!important}
  .nav-link{justify-content:space-between;width:100%;padding:12px}
  .topbar-in{font-size:.74rem;gap:14px;justify-content:center}
  .topbar-in .topbar-mid,.topbar-in .topbar-r{display:none}
  .form-split{grid-template-columns:1fr;gap:32px}
  .branches{grid-template-columns:1fr}
  .areas{grid-template-columns:repeat(2,1fr)}
  .bwall{grid-template-columns:repeat(3,1fr)}
  .brand-head{gap:16px}
  .logo img{height:36px}
}
@media (max-width:640px){
  .sec{padding-block:44px}
  .hero-in{padding-block:44px 52px}
  .cards,.posts,.lines,.feats{grid-template-columns:1fr}
  .bwall{grid-template-columns:repeat(2,1fr);gap:10px}
  .bwall-item{min-height:100px;padding:16px 10px}
  .hero-points{grid-template-columns:1fr}
  .hero-actions{flex-direction:column;align-items:stretch}
  .hero-actions .btn,.band-actions .btn{width:100%}
  .band-actions{flex-direction:column;align-items:stretch;width:100%}
  .perks-in{grid-template-columns:1fr}
  .ask-brands{grid-template-columns:1fr 1fr}
  .ask-in{padding-block:44px}
  .ft-in{grid-template-columns:1fr 1fr}
  .lead-row{grid-template-columns:1fr}
  .band-in{flex-direction:column;align-items:flex-start}
  .areas{grid-template-columns:1fr}
  .wa span{display:none}
  .wa{padding:14px;border-radius:50%}
  .badge{display:block;margin:12px 0 0;top:0;width:fit-content}
  .logo img{height:32px}
}
"""

# ---------------------------------------------------------------------------
# JS
# ---------------------------------------------------------------------------
JS = r"""
(function(){
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function(){
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }
  var groups = document.querySelectorAll('.has-menu');
  groups.forEach(function(g){
    var btn = g.querySelector('.nav-toggle');
    if(!btn) return;
    btn.addEventListener('click', function(ev){
      ev.stopPropagation();
      var wasOpen = g.classList.contains('open');
      groups.forEach(function(x){ x.classList.remove('open'); var b=x.querySelector('.nav-toggle'); if(b) b.setAttribute('aria-expanded','false'); });
      if(!wasOpen){ g.classList.add('open'); btn.setAttribute('aria-expanded','true'); }
    });
  });
  document.addEventListener('click', function(ev){
    if(ev.target.closest && ev.target.closest('.has-menu')) return;
    groups.forEach(function(x){ x.classList.remove('open'); var b=x.querySelector('.nav-toggle'); if(b) b.setAttribute('aria-expanded','false'); });
  });
  document.addEventListener('keydown', function(ev){
    if(ev.key === 'Escape'){
      groups.forEach(function(x){ x.classList.remove('open'); });
      if(nav){ nav.classList.remove('open'); }
      if(burger){ burger.setAttribute('aria-expanded','false'); }
      document.body.style.overflow = '';
    }
  });

  // Teklif formu -> WhatsApp
  var form = document.getElementById('leadForm');
  if (form) {
    form.addEventListener('submit', function(ev){
      ev.preventDefault();
      var d = new FormData(form);
      var ad = (d.get('ad')||'').toString().trim();
      var tel = (d.get('tel')||'').toString().trim();
      if(!ad || !tel){
        alertless(form, 'Lütfen ad soyad ve telefon alanlarını doldurun.');
        return;
      }
      var lines = [
        'Merhaba, web sitesi üzerinden teklif talebi:',
        'Ad Soyad: ' + ad,
        'Telefon: ' + tel
      ];
      if(d.get('urun')) lines.push('Ürün grubu: ' + d.get('urun'));
      if(d.get('bolge')) lines.push('Bölge: ' + d.get('bolge'));
      if(d.get('not')) lines.push('Not: ' + d.get('not'));
      if(form.dataset.source) lines.push('Kaynak: ' + form.dataset.source);
      var url = 'https://wa.me/__WA__?text=' + encodeURIComponent(lines.join('\n'));
      window.open(url, '_blank', 'noopener');
      alertless(form, 'Talebiniz WhatsApp üzerinden iletilmek üzere hazırlandı.');
    });
  }
  // --- hizmet haritasi: liste <-> nokta vurgulamasi ---
  var smap = document.querySelector('.smap');
  if (smap) {
    var link = function(el, on){
      var k = el.getAttribute('data-loc');
      smap.querySelectorAll('[data-loc="' + (window.CSS && CSS.escape ? CSS.escape(k) : k) + '"]')
        .forEach(function(n){ n.classList.toggle('is-hi', on); });
    };
    smap.querySelectorAll('[data-loc]').forEach(function(el){
      el.addEventListener('mouseenter', function(){ link(el, true); });
      el.addEventListener('mouseleave', function(){ link(el, false); });
      el.addEventListener('focus', function(){ link(el, true); });
      el.addEventListener('blur', function(){ link(el, false); });
    });
  }

  function alertless(scope, msg){
    var box = scope.querySelector('.form-msg');
    if(!box){
      box = document.createElement('p');
      box.className = 'form-msg lead-note';
      scope.appendChild(box);
    }
    box.textContent = msg;
  }
})();
"""


# ---------------------------------------------------------------------------
def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)
    build_home()
    build_categories()
    build_brands()
    build_locations()
    build_blog()
    build_static()
    build_assets()
    build_seo_files()
    n = sum(len(files) for _, _, files in os.walk(OUT))
    print("Toplam dosya: %d" % n)
    print("Sitemap'teki sayfa: %d" % len(ALL_PAGES))


if __name__ == "__main__":
    main()
