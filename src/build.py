# -*- coding: utf-8 -*-
"""asyacerez.com statik site üreticisi.  Çalıştır:  python3 src/build.py"""
import os, json, html, shutil, datetime
from products import PRODUCTS, CATEGORIES, PACKAGING
from i18n_ar import AR_UI, AR_PRODUCTS, AR_T, arabize

LANGS = ("tr", "en", "ar")
LANG_NAMES = {"tr": "Türkçe", "en": "English", "ar": "العربية"}
PAGE_KEY = "home"  # main() her sayfadan önce ayarlar (hreflang + dil seçici için)

# Arapça ürün alanlarını birleştir
for _p in PRODUCTS:
    _a = AR_PRODUCTS.get(_p["slug"], {})
    for _k in ("name", "tagline", "intro", "details"):
        if _k in _a: _p[_k]["ar"] = _a[_k]
    for _k, _v in _a.get("specs", {}).items(): _p["specs"][_k]["ar"] = _v
for _k, _v in AR_UI["categories"].items(): CATEGORIES[_k]["ar"] = _v
PACKAGING["ar"] = AR_UI["packaging"]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")
DOMAIN = "https://asyacerez.com"
YEAR = datetime.date.today().year
ASSET_V = datetime.datetime.now().strftime("%Y%m%d%H%M")

# ---------------------------------------------------------------- şirket bilgileri
CO = {
    "legal": "ASYA ÇEREZ DIŞ TİCARET LİMİTED ŞİRKETİ",
    "brand": "Asya Çerez",
    "street": "Mimar Kemalettin Mah. Şair Haşmet Sk. Yüksel İş Merkezi No:27/501",
    "district": "Fatih", "city": "İstanbul", "country": {"tr": "Türkiye", "en": "Türkiye", "ar": "تركيا"},
    "email": "asyacerezcilik@gmail.com",
    # Boş bırakılan alanlar sitede gösterilmez:
    "phone": "",          # örn. "+90 212 000 00 00"
    "whatsapp": "",       # örn. "905320000000" (başında + olmadan)
    "instagram": "",      # örn. "https://instagram.com/asyacerez"
    "linkedin": "",
    "form_endpoint": "https://formsubmit.co/ajax/asyacerezcilik@gmail.com",
    "form_key": "819e3807-3470-4080-8aee-fc5dccdc4303",       # Web3Forms access key girilirse form Web3Forms'a gider (hızlı)  # örn. "https://formsubmit.co/ajax/info@asyacerez.com" — boşsa e-posta istemcisi açılır
}
ADDRESS_ONE_LINE = f'{CO["street"]}, {CO["district"]} / {CO["city"]}'
MAPS_Q = "Yüksel İş Merkezi, Şair Haşmet Sk. No:27, Mimar Kemalettin, Fatih, İstanbul"

# ---------------------------------------------------------------- rotalar
ROUTES = {
    "home":     {"tr": "/",             "en": "/en/",          "ar": "/ar/"},
    "products": {"tr": "/urunler/",     "en": "/en/products/", "ar": "/ar/products/"},
    "trade":    {"tr": "/dis-ticaret/", "en": "/en/trade/",    "ar": "/ar/trade/"},
    "quality":  {"tr": "/kalite/",      "en": "/en/quality/",  "ar": "/ar/quality/"},
    "about":    {"tr": "/hakkimizda/",  "en": "/en/about/",    "ar": "/ar/about/"},
    "contact":  {"tr": "/iletisim/",    "en": "/en/contact/",  "ar": "/ar/contact/"},
}
def product_url(p, lang):
    return f"/urunler/{p['slug']}/" if lang == "tr" else f"/{lang}/products/{p['slug_en']}/"
def url(key, lang):
    if key.startswith("product:"):
        p = next(x for x in PRODUCTS if x["slug"] == key.split(":", 1)[1])
        return product_url(p, lang)
    return ROUTES[key][lang]

e = html.escape

# ---------------------------------------------------------------- arayüz metinleri
T = {
 "tr": {
  "nav_home": "Ana Sayfa", "nav_products": "Ürünler", "nav_trade": "Dış Ticaret", "nav_quality": "Kalite",
  "nav_about": "Hakkımızda", "nav_contact": "İletişim", "cta_quote": "Teklif Al", "menu": "Menü",
  "all_products": "Tüm Ürünler", "detail": "Ürünü İncele", "request_quote": "Teklif İste",
  "tagline": "Kuruyemiş & Kuru Meyve · Dış Ticaret",
  "footer_about": "İstanbul merkezli Asya Çerez; ceviz, badem, fındık, Antep fıstığı, kaju, çekirdek ve kuru meyvede toptan ithalat ve ihracat yapan bir dış ticaret şirketidir.",
  "footer_links": "Kurumsal", "footer_products": "Ürünler", "footer_contact": "İletişim",
  "rights": "Tüm hakları saklıdır.", "skip": "İçeriğe geç",
  "email": "E-posta", "phone": "Telefon", "address": "Adres", "whatsapp": "WhatsApp",
 },
 "en": {
  "nav_home": "Home", "nav_products": "Products", "nav_trade": "Foreign Trade", "nav_quality": "Quality",
  "nav_about": "About Us", "nav_contact": "Contact", "cta_quote": "Get a Quote", "menu": "Menu",
  "all_products": "All Products", "detail": "View Product", "request_quote": "Request a Quote",
  "tagline": "Nuts & Dried Fruits · Foreign Trade",
  "footer_about": "Istanbul-based Asya Çerez is a trading company engaged in the wholesale import and export of walnuts, almonds, hazelnuts, pistachios, cashews, seeds and dried fruits.",
  "footer_links": "Company", "footer_products": "Products", "footer_contact": "Contact",
  "rights": "All rights reserved.", "skip": "Skip to content",
  "email": "Email", "phone": "Phone", "address": "Address", "whatsapp": "WhatsApp",
 },
}

T["ar"] = AR_T

# ---------------------------------------------------------------- ikonlar (inline SVG, stroke)
def icon(name, size=24):
    P = {
     "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
     "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
     "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
     "ship": '<path d="M2 21c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1 .6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M19.38 20A11.6 11.6 0 0 0 21 14l-9-4-9 4c0 2.9.94 5.34 2.81 7.76"/><path d="M19 13V7a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v6"/><path d="M12 10v4"/><path d="M12 2v3"/>',
     "box": '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
     "flask": '<path d="M10 2v7.31"/><path d="M14 9.3V1.99"/><path d="M8.5 2h7"/><path d="M14 9.3a6.5 6.5 0 1 1-4 0"/><path d="M5.52 16h12.96"/>',
     "handshake": '<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2"/><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path d="M3 4h8"/>',
     "tag": '<path d="M12.59 2.59A2 2 0 0 0 11.17 2H4a2 2 0 0 0-2 2v7.17a2 2 0 0 0 .59 1.42l8.7 8.7a2.43 2.43 0 0 0 3.42 0l6.58-6.58a2.43 2.43 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/>',
     "doc": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 13H8"/><path d="M16 17H8"/><path d="M16 13h-2"/>',
     "thermo": '<path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>',
     "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
     "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
     "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
     "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
     "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
     "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
     "check": '<path d="M20 6 9 17l-5-5"/>',
     "chev": '<path d="m6 9 6 6 6-6"/>',
     "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
     "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
     "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
     "sparkle": '<path d="M9.94 14.06 4 20"/><path d="m14 4-.7 2.1a3 3 0 0 1-1.9 1.9L9.3 8.7l2.1.7a3 3 0 0 1 1.9 1.9L14 13.4l.7-2.1a3 3 0 0 1 1.9-1.9l2.1-.7-2.1-.7a3 3 0 0 1-1.9-1.9Z"/>',
     "wa": '<path d="M3 21l1.65-3.8a9 9 0 1 1 3.4 2.9L3 21"/><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0-1 0v1a5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0 1"/>',
     "ig": '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>',
     "in": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/>',
    }
    return (f'<svg class="ico ico--{name}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[name]}</svg>')

# ---------------------------------------------------------------- iskelet
def lang_list(lang):
    out = ""
    for l in LANGS:
        cls = "is-on" if l == lang else ""
        out += f'<a href="{url(PAGE_KEY, l)}" lang="{l}" hreflang="{l}" class="{cls}">{LANG_NAMES[l]}</a>'
    return out

def head(lang, title, desc, path, alt_path, og_img="/assets/img/hero.webp", jsonld=None, noindex=False):
    full_title = title if "Asya Çerez" in title else f"{title} | Asya Çerez"
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    return f"""<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="canonical" href="{DOMAIN}{path}">
{''.join(f'<link rel="alternate" hreflang="{l}" href="{DOMAIN}{url(PAGE_KEY, l)}">' for l in LANGS)}
<link rel="alternate" hreflang="x-default" href="{DOMAIN}{url(PAGE_KEY, 'tr')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Asya Çerez">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{DOMAIN}{path}">
<meta property="og:image" content="{DOMAIN}{og_img}">
<meta property="og:locale" content="{ {'tr':'tr_TR','en':'en_US','ar':'ar_AR'}[lang] }">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#3A2314">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/brand/favicon-32.png">
<link rel="icon" type="image/svg+xml" href="/assets/brand/logo-badge.svg">
<link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Poppins:wght@300;400;500;600{'&family=Amiri:wght@400;700&family=Tajawal:wght@300;400;500;700' if lang == 'ar' else ''}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css?v={ASSET_V}">
{ld}
</head>
"""

def brand_block(lang):
    return f"""<a class="brand" href="{url('home', lang)}" aria-label="Asya Çerez">
  <img class="brand__badge" src="/assets/brand/logo-badge.svg" alt="" width="46" height="46">
  <span class="brand__text"><span class="brand__name">ASYA ÇEREZ</span><span class="brand__sub">{ {'tr':'DIŞ TİCARET','en':'FOREIGN TRADE','ar':'للتجارة الخارجية'}[lang] }</span></span>
</a>"""

def header(lang, active, alt_path, transparent=False):
    t = T[lang]
    def li(key, label):
        cls = ' class="is-active"' if active == key else ""
        return f'<li><a href="{url(key, lang)}"{cls}>{label}</a></li>'
    # ürün mega menüsü
    cols = ""
    for ck, cv in CATEGORIES.items():
        items = "".join(f'<li><a href="{product_url(p, lang)}">{e(p["name"][lang])}</a></li>' for p in PRODUCTS if p["cat"] == ck)
        cols += f'<div class="mega__col"><p class="mega__title">{cv[lang]}</p><ul>{items}</ul></div>'
    mega = f"""<div class="mega" role="menu">
      <div class="mega__inner">{cols}
        <a class="mega__feature" href="{url('products', lang)}">
          <img src="/assets/img/products/karisik-kuruyemis-1-sm.webp" alt="" loading="lazy">
          <span>{t['all_products']} {icon('arrow', 16)}</span>
        </a>
      </div></div>"""
    pcls = ' class="is-active"' if active == "products" else ""
    def lang_sw(extra=""):
        items = "".join(
            (f'<span aria-current="true" lang="{l}" title="{LANG_NAMES[l]}">{l.upper()}</span>' if l == lang else
             f'<a href="{url(PAGE_KEY, l)}" hreflang="{l}" lang="{l}" title="{LANG_NAMES[l]}">{l.upper()}</a>') for l in LANGS)
        return f'<div class="lang{extra}" role="navigation" aria-label="Language">{icon("globe", 16)}{items}</div>' 
    return f"""<body class="{'has-hero' if transparent else ''}">
<a class="skip" href="#main">{t['skip']}</a>
<header class="site-header{' is-transparent' if transparent else ''}" id="top">
  <div class="container site-header__row">
    {brand_block(lang)}
    <nav class="nav" aria-label="{t['menu']}">
      <ul class="nav__list">
        {li('home', t['nav_home'])}
        <li class="has-mega"><a href="{url('products', lang)}"{pcls}>{t['nav_products']} {icon('chev', 14)}</a>{mega}</li>
        {li('trade', t['nav_trade'])}
        {li('quality', t['nav_quality'])}
        {li('about', t['nav_about'])}
        {li('contact', t['nav_contact'])}
      </ul>
    </nav>
    <div class="site-header__actions">
      {lang_sw()}
      <a class="btn btn--gold btn--sm hide-sm" href="{url('contact', lang)}">{t['cta_quote']}</a>
      <button class="burger" aria-label="{t['menu']}" aria-expanded="false" aria-controls="drawer"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" hidden>
  <nav class="drawer__nav">
    <a href="{url('home', lang)}">{t['nav_home']}</a>
    <a href="{url('products', lang)}">{t['nav_products']}</a>
    <div class="drawer__sub">{''.join(f'<a href="{product_url(p, lang)}">{e(p["name"][lang])}</a>' for p in PRODUCTS)}</div>
    <a href="{url('trade', lang)}">{t['nav_trade']}</a>
    <a href="{url('quality', lang)}">{t['nav_quality']}</a>
    <a href="{url('about', lang)}">{t['nav_about']}</a>
    <a href="{url('contact', lang)}">{t['nav_contact']}</a>
  </nav>
  <div class="drawer__foot">
    <a class="btn btn--gold" href="{url('contact', lang)}">{t['cta_quote']}</a>
    <div class="drawer__langs">{lang_list(lang)}</div>
  </div>
</div>
<main id="main">
"""

def contact_lines(lang, cls="footer__contact"):
    t = T[lang]
    out = f'<ul class="{cls}">'
    out += f'<li>{icon("pin", 18)}<span>{e(CO["street"])}<br>{CO["district"]} / {CO["city"]} — {CO["country"][lang]}</span></li>'
    out += f'<li>{icon("mail", 18)}<a href="mailto:{CO["email"]}">{CO["email"]}</a></li>'
    if CO["phone"]:
        out += f'<li>{icon("phone", 18)}<a href="tel:{CO["phone"].replace(" ", "")}">{CO["phone"]}</a></li>'
    if CO["whatsapp"]:
        out += f'<li>{icon("wa", 18)}<a href="https://wa.me/{CO["whatsapp"]}" target="_blank" rel="noopener">{t["whatsapp"]}</a></li>'
    return out + "</ul>"

def footer(lang):
    t = T[lang]
    prods = "".join(f'<li><a href="{product_url(p, lang)}">{e(p["name"][lang])}</a></li>' for p in PRODUCTS[:8])
    social = ""
    if CO["instagram"]: social += f'<a href="{CO["instagram"]}" target="_blank" rel="noopener" aria-label="Instagram">{icon("ig", 20)}</a>'
    if CO["linkedin"]:  social += f'<a href="{CO["linkedin"]}" target="_blank" rel="noopener" aria-label="LinkedIn">{icon("in", 20)}</a>'
    wa_float = (f'<a class="wa-float" href="https://wa.me/{CO["whatsapp"]}" target="_blank" rel="noopener" aria-label="WhatsApp">{icon("wa", 26)}</a>'
                if CO["whatsapp"] else "")
    return f"""</main>
<footer class="site-footer">
  <div class="container footer__grid">
    <div class="footer__brand">
      <img src="/assets/brand/logo-badge.svg" alt="Asya Çerez" width="88" height="88" loading="lazy">
      <p>{t['footer_about']}</p>
      {f'<div class="footer__social">{social}</div>' if social else ''}
    </div>
    <div><p class="footer__title">{t['footer_links']}</p><ul class="footer__links">
      <li><a href="{url('about', lang)}">{t['nav_about']}</a></li>
      <li><a href="{url('trade', lang)}">{t['nav_trade']}</a></li>
      <li><a href="{url('quality', lang)}">{t['nav_quality']}</a></li>
      <li><a href="{url('products', lang)}">{t['nav_products']}</a></li>
      <li><a href="{url('contact', lang)}">{t['nav_contact']}</a></li></ul></div>
    <div><p class="footer__title">{t['footer_products']}</p><ul class="footer__links">{prods}</ul></div>
    <div><p class="footer__title">{t['footer_contact']}</p>{contact_lines(lang)}</div>
  </div>
  <div class="container footer__bottom">
    <p>© {YEAR} {CO['legal']}. {t['rights']}</p>
    <div class="footer__langs">{icon("globe", 16)}{lang_list(lang)}</div>
  </div>
</footer>
{wa_float}
<script src="/assets/js/main.js?v={ASSET_V}" defer></script>
</body>
</html>
"""

def page_hero(lang, eyebrow, title, lead, img, crumbs):
    bc = "".join(f'<li><a href="{h}">{e(n)}</a></li>' if h else f'<li aria-current="page">{e(n)}</li>' for n, h in crumbs)
    return f"""<section class="page-hero">
  <img class="page-hero__bg" src="/assets/img/{img}" alt="" fetchpriority="high">
  <div class="container page-hero__inner">
    <ol class="crumbs">{bc}</ol>
    <p class="eyebrow eyebrow--light">{eyebrow}</p>
    <h1>{title}</h1>
    {f'<p class="page-hero__lead">{lead}</p>' if lead else ''}
  </div>
</section>"""

def product_card(p, lang, extra_cls=""):
    t = T[lang]
    return f"""<article class="pcard reveal {extra_cls}" data-cat="{p['cat']}" data-name="{e(p['name']['tr'].lower() + ' ' + p['name']['en'].lower() + ' ' + p['name'].get('ar', ''))}">
  <a href="{product_url(p, lang)}" class="pcard__link">
    <div class="pcard__media"><img src="/assets/img/products/{p['img']}-1-sm.webp" alt="{e(p['name'][lang])}" loading="lazy" width="640" height="640"></div>
    <div class="pcard__body">
      <p class="pcard__cat">{CATEGORIES[p['cat']][lang]}</p>
      <h3 class="pcard__name">{e(p['name'][lang])}</h3>
      {f'<p class="pcard__latin">{p["latin"]}</p>' if p['latin'] else ''}
      <p class="pcard__tag">{e(p['tagline'][lang])}</p>
      <span class="pcard__more">{t['detail']} {icon('arrow', 16)}</span>
    </div>
  </a>
</article>"""

def cta_band(lang):
    if lang == "tr":
        h, p, b1 = "Numune ve fiyat teklifi için bize ulaşın", "İhtiyacınız olan ürünü, kalibreyi, miktarı ve teslim şeklini iletin; size en kısa sürede ürün şartnamesi ve fiyat teklifiyle dönüş yapalım.", "Teklif Formu"
    else:
        h, p, b1 = "Contact us for samples and a quotation", "Tell us the product, grade, quantity and delivery terms you need — we'll come back promptly with a specification sheet and price offer.", "Quotation Form"
    wa = (f'<a class="btn btn--ghost-light" href="https://wa.me/{CO["whatsapp"]}" target="_blank" rel="noopener">{icon("wa", 18)} WhatsApp</a>' if CO["whatsapp"]
          else f'<a class="btn btn--ghost-light" href="mailto:{CO["email"]}">{icon("mail", 18)} {CO["email"]}</a>')
    return f"""<section class="cta-band">
  <img class="cta-band__bg" src="/assets/img/ship-sunset.webp" alt="" loading="lazy">
  <div class="container cta-band__inner reveal">
    <img class="cta-band__badge" src="/assets/brand/logo-badge.svg" alt="" width="84" height="84" loading="lazy">
    <h2>{h}</h2><p>{p}</p>
    <div class="btn-row btn-row--center"><a class="btn btn--gold" href="{url('contact', lang)}">{b1} {icon('arrow', 18)}</a>{wa}</div>
  </div>
</section>"""

def org_ld():
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": CO["legal"], "alternateName": "Asya Çerez",
          "url": DOMAIN, "logo": f"{DOMAIN}/assets/brand/favicon-512.png", "email": CO["email"],
          "address": {"@type": "PostalAddress", "streetAddress": CO["street"], "addressLocality": CO["district"],
                      "addressRegion": CO["city"], "addressCountry": "TR"}}
    if CO["phone"]: ld["telephone"] = CO["phone"]
    return ld

# ================================================================= SAYFALAR
def page_home(lang):
    t = T[lang]; tr = lang == "tr"
    featured = [p for p in PRODUCTS if p["featured"]]
    cards = "".join(product_card(p, lang) for p in featured)
    marquee_items = "".join(f'<span>{e(p["name"][lang])}</span><i>✦</i>' for p in PRODUCTS)
    cat_imgs = {"kuruyemis": "findik-1", "cekirdek": "ay-cekirdegi-1", "kurumeyve": "kuru-kayisi-1"}
    cat_desc = {
        "kuruyemis": ("Ceviz, badem, fındık, Antep fıstığı, kaju ve yer fıstığı", "Walnuts, almonds, hazelnuts, pistachios, cashews and peanuts"),
        "cekirdek": ("Ay çekirdeği, kabak çekirdeği ve Çorum leblebisi", "Sunflower seeds, pumpkin seeds and Çorum leblebi"),
        "kurumeyve": ("Malatya kayısısı, Aydın inciri, Sultana üzüm ve hurma", "Malatya apricots, Aydın figs, Sultana raisins and dates"),
    }
    cats = ""
    for ck, cv in CATEGORIES.items():
        n = sum(1 for p in PRODUCTS if p["cat"] == ck)
        cats += f"""<a class="cat reveal" href="{url('products', lang)}#{ck}">
          <img src="/assets/img/products/{cat_imgs[ck]}.webp" alt="" loading="lazy">
          <span class="cat__body"><span class="cat__count">{n} { {'tr':'ürün','en':'products','ar':'منتجات'}[lang] }</span>
          <span class="cat__name">{cv[lang]}</span><span class="cat__desc">{cat_desc[ck][0 if tr else 1]}</span>
          <span class="cat__go">{icon('arrow', 20)}</span></span></a>"""

    why = [
        ("leaf", "Menşeinden seçilmiş ürün", "Ürünleri, yetiştiği bölgenin en iyi hasadından ve güvenilir üreticilerden seçiyoruz.",
                 "Sourced at origin", "We select from the best harvests of each growing region and from trusted producers."),
        ("flask", "Parti bazlı analiz", "Nem, aflatoksin, yabancı madde ve duyusal kontroller her partide uygulanır; talep halinde laboratuvar raporu.",
                  "Lot-by-lot testing", "Moisture, aflatoxin, foreign matter and sensory checks on every lot, with lab reports on request."),
        ("box", "Toptan ambalaj & yükleme", "Vakumlu karton, çuval ve big bag; paletli, parsiyel veya tam konteyner sevkiyat.",
                "Bulk packing & loading", "Vacuum cartons, bags and big bags; palletised, LCL or full-container shipments."),
        ("ship", "Uçtan uca lojistik", "Konteyner planlama, gümrük ve ihracat evrakları; EXW'dan DAP'a tüm teslim şekilleri.",
                 "End-to-end logistics", "Container planning, customs and export documents — every term from EXW to DAP."),
        ("scale", "Şeffaf fiyatlandırma", "Piyasa koşullarına dayalı, net şartnameli ve sürprizsiz teklifler.",
                  "Transparent pricing", "Market-based offers with clear specifications and no surprises."),
        ("handshake", "Uzun vadeli ortaklık", "Tek seferlik satış değil; sezon planlaması ve düzenli tedarikle kalıcı iş birliği.",
                      "Long-term partnership", "Not one-off deals — season planning and steady supply for lasting cooperation."),
    ]
    why_html = "".join(f"""<div class="feature reveal"><div class="feature__icon">{icon(i, 26)}</div>
        <h3>{a if tr else c}</h3><p>{b if tr else d}</p></div>""" for i, a, b, c, d in why)

    steps = [
        ("Talep & Şartname", "Ürün, kalibre, miktar, ambalaj ve teslim şeklini birlikte netleştiriyoruz.", "Enquiry & Spec", "We agree product, grade, quantity, packaging and delivery terms."),
        ("Numune & Teklif", "Onayınız için numune gönderiyor, şeffaf bir fiyat teklifi sunuyoruz.", "Sample & Offer", "We send samples for approval with a transparent price offer."),
        ("Sözleşme", "Incoterms, ödeme koşulları ve sevkiyat takvimi sözleşmeye bağlanır.", "Contract", "Incoterms, payment terms and shipping schedule are contracted."),
        ("Hazırlık & Kontrol", "Ürün seçimi, analiz, ambalajlama ve yükleme öncesi son kontrol.", "Preparation & QC", "Selection, testing, packing and pre-loading inspection."),
        ("Sevkiyat & Evrak", "Konteyner yükleme, gümrük işlemleri ve tüm ihracat evrakları.", "Shipment & Docs", "Container loading, customs clearance and full export documentation."),
    ]
    steps_html = "".join(f"""<li class="step reveal"><span class="step__num">{i+1:02d}</span><h3>{a if tr else c}</h3><p>{b if tr else d}</p></li>"""
                         for i, (a, b, c, d) in enumerate(steps))
    stats = [(str(len(PRODUCTS)), "ürün grubu", "product groups"), ("2", "yönlü ticaret: ithalat & ihracat", "way trade: import & export"),
             ("6", "Incoterms teslim şekli", "Incoterms options"), ("B2B", "yalnızca toptan satış", "wholesale only")]
    stats_html = "".join(f'<div class="stat"><span class="stat__num">{n}</span><span class="stat__label">{a if tr else b}</span></div>' for n, a, b in stats)

    markets = (["Avrupa Birliği", "Körfez Ülkeleri", "Orta Doğu", "Kuzey Afrika", "Orta Asya & Kafkasya", "Balkanlar", "Rusya & BDT"] if tr
               else ["European Union", "Gulf States", "Middle East", "North Africa", "Central Asia & Caucasus", "Balkans", "Russia & CIS"])

    alt = url("home", "en" if tr else "tr")
    body = head(lang,
        "Asya Çerez | Kuruyemiş & Kuru Meyve Dış Ticaret" if tr else "Asya Çerez | Nuts & Dried Fruits Exporter from Türkiye",
        ("Asya Çerez Dış Ticaret Ltd. Şti. — ceviz, badem, fındık, Antep fıstığı, kaju, çekirdek ve kuru meyvede toptan tedarik, ithalat ve ihracat. İstanbul." if tr else
         "Asya Çerez Foreign Trade Ltd. — wholesale supply, import and export of walnuts, almonds, hazelnuts, pistachios, cashews, seeds and dried fruits from Istanbul, Türkiye."),
        url("home", lang), alt, jsonld=[org_ld()])
    body += header(lang, "home", alt, transparent=True)
    body += f"""
<section class="hero">
  <img class="hero__bg" src="/assets/img/hero.webp" alt="" fetchpriority="high">
  <div class="hero__shade"></div>
  <div class="container hero__inner">
    <div class="hero__content">
      <p class="eyebrow eyebrow--light hero__anim" style="--d:.05s">{'Toptan İthalat &amp; İhracat · İstanbul' if tr else 'Wholesale Import &amp; Export · Istanbul'}</p>
      <h1 class="hero__title hero__anim" style="--d:.15s">{'Doğanın en seçkin <em>kuruyemişleri</em>, dünyanın dört bir yanına.' if tr else "Nature's finest <em>nuts</em> &amp; dried fruits, delivered worldwide."}</h1>
      <p class="hero__lead hero__anim" style="--d:.3s">{"Ceviz, badem, fındık, Antep fıstığı, kaju, çekirdek ve kuru meyvede toptan ithalat ve ihracat. Menşeinden seçilmiş, analizli ürünleri ton bazında, konteyner yüklemeli olarak tedarik ediyoruz." if tr else "Wholesale import and export of walnuts, almonds, hazelnuts, pistachios, cashews, seeds and dried fruits — selected at origin, lab-tested and supplied by the tonne in full container loads."}</p>
      <div class="btn-row hero__anim" style="--d:.45s">
        <a class="btn btn--gold" href="{url('products', lang)}">{'Ürünleri İncele' if tr else 'Explore Products'} {icon('arrow', 18)}</a>
        <a class="btn btn--ghost-light" href="{url('contact', lang)}">{t['request_quote']}</a>
      </div>
    </div>
    <div class="hero__seal hero__anim" style="--d:.6s" aria-hidden="true">
      <svg viewBox="0 0 200 200" class="hero__ring"><defs><path id="circ" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>
      <text><textPath href="#circ" textLength="486" lengthAdjust="spacingAndGlyphs">{'TOPTAN İTHALAT · İHRACAT · PREMIUM KALİTE · ' if tr else 'WHOLESALE IMPORT · EXPORT · PREMIUM QUALITY · '}</textPath></text></svg>
      <img src="/assets/brand/logo-badge.svg" alt="" width="120" height="120">
    </div>
  </div>
  <div class="hero__stats"><div class="container stats">{stats_html}</div></div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee__track">{marquee_items}{marquee_items}</div></div>

<section class="section">
  <div class="container split">
    <div class="split__media reveal">
      <img class="split__img1" src="/assets/img/market.webp" alt="{'Kuruyemiş ve kuru meyve çeşitleri' if tr else 'Assorted nuts and dried fruits'}" loading="lazy">
      <img class="split__img2" src="/assets/img/products/ceviz-3-sm.webp" alt="" loading="lazy">
      <div class="split__badge"><span>{'Anadolu’dan' if tr else 'From Anatolia'}</span><strong>{'Dünyaya' if tr else 'to the World'}</strong></div>
    </div>
    <div class="split__text reveal">
      <p class="eyebrow">{'Asya Çerez Hakkında' if tr else 'About Asya Çerez'}</p>
      <h2>{'Anadolu’nun bereketini güvenle dünyaya taşıyoruz' if tr else 'Carrying the richness of Anatolia to the world — reliably'}</h2>
      <p>{"Asya Çerez Dış Ticaret Ltd. Şti., İstanbul'un tarihi ticaret merkezi Fatih'te kurulmuş bir kuruyemiş ve kuru meyve dış ticaret şirketidir. Türkiye'nin dünyaca ünlü fındık, Antep fıstığı, kayısı, incir ve üzümünü uluslararası pazarlara ulaştırırken; kaju, badem, ceviz ve hurma gibi ürünleri de dünyanın önde gelen üretim bölgelerinden Türkiye'ye getiriyoruz." if tr else "Asya Çerez Foreign Trade Ltd. is a nuts and dried fruits trading company based in Fatih, Istanbul's historic trading quarter. We bring Türkiye's world-famous hazelnuts, pistachios, apricots, figs and raisins to international markets, while importing cashews, almonds, walnuts and dates from the world's leading growing regions."}</p>
      <ul class="checks">
        <li>{icon('check', 18)} {'İthalat, ihracat ve toptan tedarik tek çatı altında' if tr else 'Import, export and wholesale supply under one roof'}</li>
        <li>{icon('check', 18)} {'Ton bazında; palet, parsiyel ve konteyner yüklemeli satış' if tr else 'Sold by the tonne — palletised, LCL or full container'}</li>
        <li>{icon('check', 18)} {'Her partide analiz ve izlenebilirlik' if tr else 'Testing and traceability on every lot'}</li>
      </ul>
      <a class="link-arrow" href="{url('about', lang)}">{'Hikâyemizi okuyun' if tr else 'Read our story'} {icon('arrow', 18)}</a>
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">{'Öne Çıkan Ürünler' if tr else 'Featured Products'}</p>
      <h2>{'Seçkin ürün yelpazemiz' if tr else 'Our selected range'}</h2>
      <p>{'Her ürün için çeşit, kalibre, menşe ve ambalaj seçeneklerini detay sayfasında inceleyebilirsiniz.' if tr else 'See varieties, grades, origins and packaging options on each product page.'}</p>
    </div>
    <div class="grid grid--products">{cards}</div>
    <div class="center mt-lg"><a class="btn btn--dark" href="{url('products', lang)}">{t['all_products']} ({len(PRODUCTS)}) {icon('arrow', 18)}</a></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">{'Kategoriler' if tr else 'Categories'}</p><h2>{'Üç ana ürün grubu' if tr else 'Three product families'}</h2></div>
    <div class="cats">{cats}</div>
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    <div class="section-head section-head--light reveal">
      <p class="eyebrow">{'Neden Asya Çerez?' if tr else 'Why Asya Çerez?'}</p>
      <h2>{'Güven, kalite ve süreklilik' if tr else 'Trust, quality and continuity'}</h2>
    </div>
    <div class="features">{why_html}</div>
  </div>
</section>

<section class="section process">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">{'Çalışma Sürecimiz' if tr else 'How We Work'}</p>
      <h2>{'Talepten teslimata beş adım' if tr else 'Five steps from enquiry to delivery'}</h2>
    </div>
    <ol class="steps">{steps_html}</ol>
  </div>
</section>

<section class="section section--cream">
  <div class="container split split--rev">
    <div class="split__text reveal">
      <p class="eyebrow">{'Toptan Ambalaj & Yükleme' if tr else 'Bulk Packing & Loading'}</p>
      <h2>{'İhracata uygun ambalaj, güvenli yükleme' if tr else 'Export-grade packing, secure loading'}</h2>
      <p>{'Ürünlerimizi yalnızca toptan olarak; vakumlu karton, çuval ve big bag ambalajlarda sunuyoruz. Paletleme, konteyner istifleme ve yükleme, ürünün tazeliğini ve güvenliğini koruyacak şekilde planlanır; koli etiketleri hedef ülke mevzuatına göre hazırlanır.' if tr else 'We sell wholesale only, in vacuum cartons, bags and big bags. Palletising, container stowage and loading are planned to protect freshness and safety, and carton labels follow destination-country regulations.'}</p>
      <ul class="pack-list">{''.join(f'<li>{icon("box", 20)}<span>{x}</span></li>' for x in PACKAGING[lang])}</ul>
    </div>
    <div class="split__media reveal">
      <img class="split__img1" src="/assets/img/bowls.webp" alt="" loading="lazy">
      <img class="split__img2" src="/assets/img/products/antep-fistigi-2-sm.webp" alt="" loading="lazy">
    </div>
  </div>
</section>

<section class="section markets">
  <div class="container markets__inner">
    <div class="reveal">
      <p class="eyebrow">{'Pazarlar' if tr else 'Markets'}</p>
      <h2>{'Odaklandığımız bölgeler' if tr else 'Regions we focus on'}</h2>
      <p>{'Türkiye merkezli konumumuz sayesinde Avrupa, Orta Doğu, Afrika ve Asya pazarlarına hızlı ve ekonomik sevkiyat planlıyoruz.' if tr else 'Our Türkiye base lets us plan fast, cost-effective shipments to Europe, the Middle East, Africa and Asia.'}</p>
      <div class="chips">{''.join(f'<span class="chip">{icon("globe", 16)} {m}</span>' for m in markets)}</div>
    </div>
    <div class="incoterms reveal">
      <p class="incoterms__title">{'Teslim Şekilleri' if tr else 'Delivery Terms'}</p>
      <div class="incoterms__grid">{''.join(f'<span>{x}</span>' for x in ['EXW','FCA','FOB','CFR','CIF','DAP'])}</div>
      <a class="link-arrow" href="{url('trade', lang)}">{'Dış ticaret hizmetlerimiz' if tr else 'Our trade services'} {icon('arrow', 18)}</a>
    </div>
  </div>
</section>
{cta_band(lang)}
"""
    body += footer(lang)
    return body

def page_products(lang):
    t = T[lang]; tr = lang == "tr"
    alt = url("products", "en" if tr else "tr")
    body = head(lang, "Ürünlerimiz — Kuruyemiş, Çekirdek ve Kuru Meyve" if tr else "Products — Nuts, Seeds and Dried Fruits",
                ("Ceviz, badem, fındık, Antep fıstığı, kaju, yer fıstığı, ay çekirdeği, kabak çekirdeği, leblebi, kuru kayısı, kuru incir, kuru üzüm ve hurma. Çeşit, kalibre ve ambalaj bilgileri." if tr else
                 "Walnuts, almonds, hazelnuts, pistachios, cashews, peanuts, sunflower and pumpkin seeds, leblebi, dried apricots, figs, raisins and dates — varieties, grades and packaging."),
                url("products", lang), alt)
    body += header(lang, "products", alt)
    body += page_hero(lang, ("Ürün Kataloğu" if tr else "Product Catalogue"), (t["nav_products"]),
                      ("Toptan ithalat ve ihracatını yaptığımız; menşeinden seçilmiş, kalibre ve kaliteye göre sınıflandırılmış ürünlerimiz." if tr else "The products we import and export wholesale — selected at origin, graded by size and quality."),
                      "hero-mix.webp", [(t["nav_home"], url("home", lang)), (t["nav_products"], None)])
    chips = f'<button class="fchip is-on" data-filter="all">{"Tümü" if tr else "All"} <span>{len(PRODUCTS)}</span></button>'
    for ck, cv in CATEGORIES.items():
        n = sum(1 for p in PRODUCTS if p["cat"] == ck)
        chips += f'<button class="fchip" data-filter="{ck}">{cv[lang]} <span>{n}</span></button>'
    cards = "".join(product_card(p, lang) for p in PRODUCTS)
    body += f"""
<section class="section section--tight">
  <div class="container">
    <div class="toolbar">
      <div class="fchips" role="group">{chips}</div>
      <label class="search">{icon('search', 18)}<input type="search" placeholder="{'Ürün ara…' if tr else 'Search products…'}" aria-label="{'Ürün ara' if tr else 'Search products'}"></label>
    </div>
    <div class="grid grid--products" id="product-grid">{cards}</div>
    <p class="empty" hidden>{'Aradığınız ürünü bulamadınız mı? Tedarik ağımızda olabilir — ' if tr else "Can't find it? It may still be in our sourcing network — "}<a href="{url('contact', lang)}">{'bize sorun' if tr else 'ask us'}</a>.</p>
  </div>
</section>
<section class="section section--cream section--tight">
  <div class="container note-row reveal">
    <div class="note">{icon('sparkle', 26)}<div><h3>{'Listede olmayan bir ürün mü arıyorsunuz?' if tr else 'Looking for something not listed?'}</h3>
    <p>{'Macadamia, pekan cevizi, Brezilya fıstığı, kuru erik, kızılcık ve daha fazlası için tedarik ağımızdan teklif alabilirsiniz.' if tr else 'We can source macadamias, pecans, Brazil nuts, prunes, cranberries and more through our network.'}</p></div></div>
    <a class="btn btn--dark" href="{url('contact', lang)}">{t['request_quote']} {icon('arrow', 18)}</a>
  </div>
</section>
{cta_band(lang)}"""
    body += footer(lang)
    return body

def page_product(p, lang):
    t = T[lang]; tr = lang == "tr"
    alt = product_url(p, "en" if tr else "tr")
    name = p["name"][lang]
    imgs = [f"{p['img']}-{i}" for i in range(1, p["gallery"] + 1)]
    thumbs = "".join(f'<button class="gal__thumb{" is-on" if i == 0 else ""}" data-src="/assets/img/products/{im}.webp" aria-label="{e(name)} {i+1}"><img src="/assets/img/products/{im}-sm.webp" alt="" loading="lazy"></button>'
                     for i, im in enumerate(imgs)) if len(imgs) > 1 else ""
    S = p["specs"]
    spec_rows = [
        ("Menşe" if tr else "Origin", S["origin"][lang]),
        ("Formlar" if tr else "Forms", S["forms"][lang]),
        ("Kalibre / Sınıf" if tr else "Grades / Sizes", S["grades"][lang]),
        ("Nem" if tr else "Moisture", S["moisture"][lang]),
        ("Raf ömrü" if tr else "Shelf life", S["shelf"][lang]),
        ("GTİP / HS Kodu" if tr else "HS Code", S["hs"]),
        ("Satış şekli" if tr else "Sales terms", "Yalnızca toptan · palet, parsiyel veya konteyner (20’ / 40’)" if tr else "Wholesale only · pallet, LCL or container (20’ / 40’)"),
    ]
    specs = "".join(f"<tr><th>{a}</th><td>{e(b)}</td></tr>" for a, b in spec_rows)
    details = "".join(f"<li>{icon('check', 18)}<span>{e(x)}</span></li>" for x in p["details"][lang])
    nut = ""
    if p["nutrition"]:
        k, pr, fa, ca, fi = p["nutrition"]
        fmt = (lambda v: f"{v:.1f}".replace(".", ",")) if tr else (lambda v: f"{v:.1f}")
        rows = [("Enerji" if tr else "Energy", f"{k} kcal", min(k / 700, 1)), ("Protein", f"{fmt(pr)} g", pr / 35),
                ("Yağ" if tr else "Fat", f"{fmt(fa)} g", fa / 70), ("Karbonhidrat" if tr else "Carbohydrate", f"{fmt(ca)} g", ca / 85),
                ("Lif" if tr else "Fibre", f"{fmt(fi)} g", fi / 16)]
        bars = "".join(f'<div class="nut__row"><span>{a}</span><span class="nut__bar"><i style="--w:{min(w,1)*100:.0f}%"></i></span><strong>{b}</strong></div>' for a, b, w in rows)
        nut = f"""<div class="panel" id="tab-nut" role="tabpanel" hidden>
          <p class="muted">{'100 g için yaklaşık besin değerleri (çiğ ürün). Değerler çeşide ve partiye göre değişebilir.' if tr else 'Approximate nutrition per 100 g (raw product). Values vary by variety and lot.'}</p>
          <div class="nut">{bars}</div></div>"""
    else:
        nut = f"""<div class="panel" id="tab-nut" role="tabpanel" hidden><p class="muted">{'Besin değerleri karışımın içeriğine göre değişir; ürün şartnamesiyle birlikte paylaşılır.' if tr else 'Nutrition depends on the blend and is shared with the product specification.'}</p></div>"""
    storage = (["Serin (0–10 °C), kuru (bağıl nem < %65) ve karanlık ortamda saklanmalıdır.",
                "Güçlü koku yayan ürünlerden uzak, zeminle temas etmeyecek şekilde paletlerde depolanmalıdır.",
                "Açılan ambalajlar hava almayacak şekilde kapatılmalıdır.",
                "Uzun süreli depolamada soğuk hava deposu önerilir."] if tr else
               ["Store cool (0–10 °C), dry (RH < 65%) and away from light.",
                "Keep on pallets, off the floor and away from strong odours.",
                "Reseal opened packs airtight.",
                "Cold storage recommended for long-term holding."])
    pack = "".join(f'<li>{icon("box", 18)}<span>{x}</span></li>' for x in PACKAGING[lang])
    related = [x for x in PRODUCTS if x["cat"] == p["cat"] and x["slug"] != p["slug"]]
    related = (related + [x for x in PRODUCTS if x["featured"] and x not in related and x["slug"] != p["slug"]])[:4]
    rel = "".join(product_card(x, lang) for x in related)
    wa_btn = (f'<a class="btn btn--outline" href="https://wa.me/{CO["whatsapp"]}?text={html.escape(("Merhaba, " + name + " için fiyat teklifi almak istiyorum.") if tr else ("Hello, I would like a quote for " + name + "."))}" target="_blank" rel="noopener">{icon("wa", 18)} WhatsApp</a>'
              if CO["whatsapp"] else f'<a class="btn btn--outline" href="mailto:{CO["email"]}?subject={html.escape(name)}">{icon("mail", 18)} {t["email"]}</a>')
    ld = {"@context": "https://schema.org", "@type": "Product", "name": name, "image": [f"{DOMAIN}/assets/img/products/{i}.webp" for i in imgs],
          "description": p["intro"][lang], "brand": {"@type": "Brand", "name": "Asya Çerez"}, "category": CATEGORIES[p["cat"]][lang]}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": t["nav_home"], "item": DOMAIN + url("home", lang)},
        {"@type": "ListItem", "position": 2, "name": t["nav_products"], "item": DOMAIN + url("products", lang)},
        {"@type": "ListItem", "position": 3, "name": name, "item": DOMAIN + product_url(p, lang)}]}
    title = {"tr": f"Toptan {name} — İthalat ve İhracat", "en": f"Wholesale {name} — Import & Export", "ar": f"{name} بالجملة — استيراد وتصدير"}[lang]
    body = head(lang, title, p["intro"][lang][:155].rsplit(" ", 1)[0] + "…", product_url(p, lang), alt,
                og_img=f"/assets/img/products/{imgs[0]}.webp", jsonld=[ld, bc])
    body += header(lang, "products", alt)
    body += f"""
<section class="pd">
  <div class="container">
    <ol class="crumbs crumbs--dark">
      <li><a href="{url('home', lang)}">{t['nav_home']}</a></li>
      <li><a href="{url('products', lang)}">{t['nav_products']}</a></li>
      <li><a href="{url('products', lang)}#{p['cat']}">{CATEGORIES[p['cat']][lang]}</a></li>
      <li aria-current="page">{e(name)}</li>
    </ol>
    <div class="pd__grid">
      <div class="gal">
        <div class="gal__main"><img id="gal-main" src="/assets/img/products/{imgs[0]}.webp" alt="{e(name)}" width="1600" height="1600" fetchpriority="high"></div>
        {f'<div class="gal__thumbs">{thumbs}</div>' if thumbs else ''}
      </div>
      <div class="pd__info">
        <p class="eyebrow">{CATEGORIES[p['cat']][lang]}</p>
        <h1 class="pd__title">{e(name)}</h1>
        {f'<p class="pd__latin">{p["latin"]}</p>' if p['latin'] else ''}
        <p class="pd__lead">{e(p['intro'][lang])}</p>
        <div class="pd__quick">
          <div>{icon('globe', 20)}<span><small>{'Menşe' if tr else 'Origin'}</small>{e(S['origin'][lang].split(',')[0].split('(')[0].strip())}{' +' if ',' in S['origin'][lang] else ''}</span></div>
          <div>{icon('tag', 20)}<span><small>GTİP / HS</small>{S['hs'].split(' ')[0]}</span></div>
          <div>{icon('clock', 20)}<span><small>{'Raf ömrü' if tr else 'Shelf life'}</small>{e(S['shelf'][lang].split('·')[0].replace('Uygun koşullarda ','').replace(' under proper storage','').replace('Natürel: ','').replace('Natural: ','').strip())}</span></div>
        </div>
        <div class="btn-row">
          <a class="btn btn--gold" href="{url('contact', lang)}?urun={p['slug']}">{t['request_quote']} {icon('arrow', 18)}</a>
          {wa_btn}
        </div>
        <p class="pd__note">{icon('shield', 18)} {'Yalnızca toptan satış · numune ve analiz raporu talep üzerine sağlanır.' if tr else 'Wholesale only · samples and lab reports available on request.'}</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--cream section--tight">
  <div class="container pd__more">
    <div class="tabs" role="tablist">
      <button role="tab" class="tab is-on" aria-selected="true" aria-controls="tab-spec">{'Teknik Özellikler' if tr else 'Specifications'}</button>
      <button role="tab" class="tab" aria-selected="false" aria-controls="tab-det">{'Ürün Detayı' if tr else 'Details'}</button>
      <button role="tab" class="tab" aria-selected="false" aria-controls="tab-nut">{'Besin Değerleri' if tr else 'Nutrition'}</button>
      <button role="tab" class="tab" aria-selected="false" aria-controls="tab-pack">{'Ambalaj & Depolama' if tr else 'Packing & Storage'}</button>
    </div>
    <div class="panel" id="tab-spec" role="tabpanel"><table class="spec">{specs}</table>
      <p class="muted small">{'Değerler tipik şartname değerleridir; kesin değerler sözleşme ve parti analiz raporunda belirtilir.' if tr else 'Typical specification values; binding values are stated in the contract and lot analysis report.'}</p></div>
    <div class="panel" id="tab-det" role="tabpanel" hidden><ul class="checks checks--lg">{details}</ul></div>
    {nut}
    <div class="panel" id="tab-pack" role="tabpanel" hidden>
      <div class="two-col"><div><h3>{'Ambalaj seçenekleri' if tr else 'Packaging options'}</h3><ul class="pack-list">{pack}</ul></div>
      <div><h3>{'Depolama koşulları' if tr else 'Storage conditions'}</h3><ul class="checks">{''.join(f'<li>{icon("thermo", 18)}<span>{e(x)}</span></li>' for x in storage)}</ul></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head section-head--row reveal"><div><p class="eyebrow">{'İlginizi çekebilir' if tr else 'You may also like'}</p><h2>{'Diğer ürünler' if tr else 'Related products'}</h2></div>
    <a class="link-arrow" href="{url('products', lang)}">{t['all_products']} {icon('arrow', 18)}</a></div>
    <div class="grid grid--products">{rel}</div>
  </div>
</section>
{cta_band(lang)}"""
    body += footer(lang)
    return body

def page_trade(lang):
    t = T[lang]; tr = lang == "tr"
    alt = url("trade", "en" if tr else "tr")
    services = [
        ("ship", "İhracat", "Türkiye'nin fındık, Antep fıstığı, kuru kayısı, kuru incir, kuru üzüm ve leblebisini dünya pazarlarına ulaştırıyoruz.",
                 "Export", "We deliver Türkiye's hazelnuts, pistachios, dried apricots, figs, raisins and leblebi to world markets."),
        ("globe", "İthalat", "Kaju, badem, ceviz ve hurmayı dünyanın önde gelen üretim bölgelerinden Türkiye pazarına getiriyoruz.",
                  "Import", "We bring cashews, almonds, walnuts and dates from the world's leading growing regions into Türkiye."),
        ("truck", "Toptan Tedarik", "Kuruyemiş toptancıları, distribütörler, paketleme firmaları ve gıda sanayicileri için ton bazında düzenli tedarik.",
                  "Wholesale Supply", "Regular supply by the tonne for nut wholesalers, distributors, packers and food manufacturers."),
        ("search", "Kaynak Bulma", "Aradığınız ürünü, kalibreyi ve menşei üretici ağımızdan bulur; fiyat ve kalite karşılaştırmasıyla sunarız.",
                "Sourcing", "We find the product, grade and origin you need through our producer network and present price and quality options."),
        ("doc", "Gümrük & Evrak", "İhracat ve ithalat evraklarının hazırlanması, gümrük müşavirliği koordinasyonu.",
                "Customs & Documents", "Preparation of export/import documents and coordination with customs brokers."),
        ("box", "Numune Hizmeti", "Sipariş öncesi ürün numunesi ve analiz raporu gönderimi.",
                "Sample Service", "Pre-order samples and lab analysis reports shipped to you."),
    ]
    svc = "".join(f'<div class="svc reveal"><div class="feature__icon">{icon(i, 26)}</div><h3>{a if tr else c}</h3><p>{b if tr else d}</p></div>' for i, a, b, c, d in services)
    inc = [("EXW", "Fabrikada teslim", "Ex Works", "Alıcı, ürünü depomuzdan teslim alır; tüm taşıma alıcıya aittir.", "Buyer collects from our warehouse and handles all carriage."),
           ("FCA", "Taşıyıcıya teslim", "Free Carrier", "Ürün, alıcının belirlediği taşıyıcıya ihracat işlemleri tamamlanmış olarak teslim edilir.", "Goods handed to the buyer's carrier, export-cleared."),
           ("FOB", "Gemide teslim", "Free On Board", "Ürün, Türkiye limanında gemiye yüklenmiş olarak teslim edilir.", "Goods delivered loaded on board at the Turkish port."),
           ("CFR", "Mal bedeli ve navlun", "Cost and Freight", "Varış limanına kadar navlun satıcıya aittir.", "Seller pays sea freight to the destination port."),
           ("CIF", "Mal bedeli, sigorta ve navlun", "Cost, Insurance, Freight", "CFR'ye ek olarak deniz sigortası satıcı tarafından yapılır.", "As CFR, plus marine insurance arranged by the seller."),
           ("DAP", "Belirlenen yerde teslim", "Delivered at Place", "Ürün, alıcının belirttiği adrese gümrük vergileri hariç teslim edilir.", "Delivered to the buyer's named place, duties excluded.")]
    inc_rows = "".join(f'<tr><th><span class="inc">{a}</span></th><td><strong>{b if tr else c}</strong><br><span class="muted">{d if tr else f}</span></td></tr>' for a, b, c, d, f in inc)
    docs = (["Ticari fatura ve çeki listesi (packing list)", "Menşe şahadetnamesi (Certificate of Origin), EUR.1 / A.TR", "Fitosanitar sertifika (bitki sağlık sertifikası)",
             "Analiz raporu (aflatoksin, nem, mikrobiyoloji)", "Konşimento (Bill of Lading) / CMR", "Sağlık sertifikası ve helal sertifikası (talep halinde)"] if tr else
            ["Commercial invoice and packing list", "Certificate of Origin, EUR.1 / A.TR", "Phytosanitary certificate",
             "Analysis report (aflatoxin, moisture, microbiology)", "Bill of Lading / CMR", "Health certificate and halal certificate (on request)"])
    pay = (["Peşin / avans ödeme (T/T)", "Akreditif (L/C)", "Vesaik mukabili (CAD)", "Kısmi avans + bakiye yükleme sonrası"] if tr else
           ["Advance payment (T/T)", "Letter of Credit (L/C)", "Cash Against Documents (CAD)", "Partial advance + balance after loading"])
    body = head(lang, "Dış Ticaret Hizmetleri — İthalat, İhracat, Toptan" if tr else "Foreign Trade Services — Import, Export, Wholesale",
                ("Asya Çerez'in kuruyemiş ve kuru meyvede ihracat, ithalat, toptan tedarik, kaynak bulma, gümrük ve lojistik hizmetleri; Incoterms teslim şekilleri ve ihracat evrakları." if tr else
                 "Asya Çerez export, import, wholesale, sourcing, customs and logistics services for nuts and dried fruits — Incoterms and export documents."),
                url("trade", lang), alt, og_img="/assets/img/ship.webp")
    body += header(lang, "trade", alt)
    body += page_hero(lang, ("Hizmetlerimiz" if tr else "Our Services"), t["nav_trade"],
                      ("Kaynaktan sevkiyata kadar tüm dış ticaret sürecini sizin için yönetiyoruz." if tr else "We manage the whole trade process for you — from sourcing to shipment."),
                      "ship.webp", [(t["nav_home"], url("home", lang)), (t["nav_trade"], None)])
    body += f"""
<section class="section">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">{'Ne yapıyoruz?' if tr else 'What we do'}</p><h2>{'Uçtan uca dış ticaret çözümleri' if tr else 'End-to-end trade solutions'}</h2></div>
    <div class="svcs">{svc}</div>
  </div>
</section>
<section class="section section--cream">
  <div class="container split">
    <div class="split__text reveal">
      <p class="eyebrow" lang="en">Incoterms® 2020</p>
      <h2>{'Size uygun teslim şekli' if tr else 'The delivery term that suits you'}</h2>
      <p>{'Tüm uluslararası teslim şekilleriyle çalışıyoruz. Konteyner (20’ / 40’) veya parsiyel sevkiyat seçenekleri, ürün ve varış noktasına göre birlikte planlanır.' if tr else 'We work with all common international terms. Full container (20’ / 40’) or LCL shipments are planned together based on product and destination.'}</p>
      <table class="spec spec--inc">{inc_rows}</table>
    </div>
    <div class="split__media split__media--tall reveal"><img class="split__img1" src="/assets/img/containers.webp" alt="" loading="lazy"><img class="split__img2" src="/assets/img/ship-aerial.webp" alt="" loading="lazy"></div>
  </div>
</section>
<section class="section">
  <div class="container two-col two-col--cards">
    <div class="card reveal"><div class="feature__icon">{icon('doc', 26)}</div><h3>{'İhracat evrakları' if tr else 'Export documents'}</h3><ul class="checks">{''.join(f'<li>{icon("check", 18)}<span>{x}</span></li>' for x in docs)}</ul></div>
    <div class="card reveal"><div class="feature__icon">{icon('scale', 26)}</div><h3>{'Ödeme koşulları' if tr else 'Payment terms'}</h3><ul class="checks">{''.join(f'<li>{icon("check", 18)}<span>{x}</span></li>' for x in pay)}</ul>
    <p class="muted small">{'Ödeme koşulları, sipariş hacmi ve iş ilişkisine göre karşılıklı mutabakatla belirlenir.' if tr else 'Payment terms are agreed mutually based on order volume and relationship.'}</p></div>
  </div>
</section>
{cta_band(lang)}"""
    body += footer(lang)
    return body

def page_quality(lang):
    t = T[lang]; tr = lang == "tr"
    alt = url("quality", "en" if tr else "tr")
    steps = [
        ("leaf", "Kaynak seçimi", "Üreticiler; bölge, hasat dönemi, işleme tesisi ve geçmiş analiz sonuçlarına göre seçilir.", "Source selection", "Producers are chosen by region, harvest, processing facility and past test results."),
        ("search", "Ön numune kontrolü", "Satın alma öncesi numunede renk, kalibre, kusur oranı ve tat kontrol edilir.", "Pre-shipment sample", "Colour, size, defect rate and taste are checked on samples before purchase."),
        ("flask", "Laboratuvar analizi", "Nem, aflatoksin (B1 ve toplam), pestisit kalıntısı ve mikrobiyolojik analizler akredite laboratuvarlarda yapılır.", "Laboratory analysis", "Moisture, aflatoxin (B1 and total), pesticide residues and microbiology tested in accredited labs."),
        ("box", "Ambalaj & etiket", "Gıdaya uygun, izlenebilirlik için parti numarası taşıyan ambalaj; hedef ülke mevzuatına uygun etiket.", "Packing & labelling", "Food-grade packaging with lot codes for traceability; labels compliant with destination rules."),
        ("thermo", "Depolama", "Isı ve nem kontrollü depolama; gerekli ürünlerde soğuk hava deposu.", "Storage", "Temperature- and humidity-controlled storage; cold storage where required."),
        ("ship", "Yükleme kontrolü", "Yükleme öncesi son görsel kontrol, konteyner temizliği ve fotoğraflı yükleme raporu.", "Loading inspection", "Final visual check, container cleanliness and photo loading report."),
    ]
    st = "".join(f'<li class="qstep reveal"><div class="feature__icon">{icon(i, 24)}</div><div><h3><span class="qstep__n">{n+1:02d}</span> {a if tr else c}</h3><p>{b if tr else d}</p></div></li>' for n, (i, a, b, c, d) in enumerate(steps))
    params = [("Nem", "Moisture", "Ürüne özel sınır değerler"), ("Aflatoksin B1 / Toplam", "Aflatoxin B1 / Total", "AB 2023/915 sınırları"),
              ("Pestisit kalıntısı", "Pesticide residues", "Hedef ülke MRL değerleri"), ("Mikrobiyoloji", "Microbiology", "Salmonella, E. coli, küf-maya"),
              ("Yabancı madde", "Foreign matter", "Optik ve el ile ayıklama"), ("Duyusal analiz", "Sensory", "Renk, koku, tat, doku")]
    pr = "".join(f'<div class="param reveal"><strong>{a if tr else b}</strong><span>{c if tr else {"Ürüne özel sınır değerler":"Product-specific limits","AB 2023/915 sınırları":"EU 2023/915 limits","Hedef ülke MRL değerleri":"Destination MRLs","Salmonella, E. coli, küf-maya":"Salmonella, E. coli, yeast & mould","Optik ve el ile ayıklama":"Optical and hand sorting","Renk, koku, tat, doku":"Colour, odour, taste, texture"}[c]}</span></div>' for a, b, c in params)
    body = head(lang, "Kalite Politikası ve Kontrol Süreci" if tr else "Quality Policy and Control Process",
                ("Asya Çerez kalite süreci: kaynak seçimi, numune kontrolü, aflatoksin ve nem analizi, izlenebilir ambalaj, kontrollü depolama ve yükleme kontrolü." if tr else
                 "Asya Çerez quality process: source selection, sample checks, aflatoxin and moisture testing, traceable packing, controlled storage and loading inspection."),
                url("quality", lang), alt, og_img="/assets/img/tasting.webp")
    body += header(lang, "quality", alt)
    body += page_hero(lang, ("Kalite" if tr else "Quality"), ("Kalite, her partide yeniden kanıtlanır" if tr else "Quality, proven again with every lot"),
                      ("Ürünlerimizin kaynağından sevkiyatına kadar izlediği kontrol adımları." if tr else "The control steps our products pass from origin to shipment."),
                      "tasting.webp", [(t["nav_home"], url("home", lang)), (t["nav_quality"], None)])
    body += f"""
<section class="section">
  <div class="container split">
    <div class="split__text reveal">
      <p class="eyebrow">{'Kalite Politikamız' if tr else 'Our Quality Policy'}</p>
      <h2>{'Gıda güvenliği pazarlık konusu değildir' if tr else 'Food safety is not negotiable'}</h2>
      <p>{'Kuruyemiş ve kuru meyve ticaretinde en kritik riskler nem, aflatoksin ve yabancı maddedir. Bu nedenle her partiyi sözleşmedeki şartnameye göre kontrol ediyor, uygun olmayan ürünü sevk etmiyoruz. Alıcılarımızla analiz sonuçlarını şeffaf şekilde paylaşıyor ve bağımsız gözetim firmalarının (SGS, Bureau Veritas, Intertek vb.) yükleme kontrollerine açık çalışıyoruz.' if tr else 'The critical risks in nut and dried fruit trade are moisture, aflatoxin and foreign matter. We check each lot against the contract specification and do not ship non-conforming goods. We share results transparently and welcome independent surveyors (SGS, Bureau Veritas, Intertek, etc.) at loading.'}</p>
      <ul class="checks"><li>{icon('check', 18)} {'Her parti için izlenebilir lot numarası' if tr else 'Traceable lot code on every lot'}</li>
      <li>{icon('check', 18)} {'AB ve hedef ülke mevzuatına uygunluk' if tr else 'Compliance with EU and destination regulations'}</li>
      <li>{icon('check', 18)} {'Bağımsız gözetime açık yükleme' if tr else 'Loading open to independent surveyors'}</li></ul>
    </div>
    <div class="split__media reveal"><img class="split__img1" src="/assets/img/products/findik-2.webp" alt="" loading="lazy"><img class="split__img2" src="/assets/img/products/badem-2-sm.webp" alt="" loading="lazy"></div>
  </div>
</section>
<section class="section section--cream">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">{'Kontrol Süreci' if tr else 'Control Process'}</p><h2>{'Kaynaktan konteynere altı adım' if tr else 'Six steps from source to container'}</h2></div>
    <ol class="qsteps">{st}</ol>
  </div>
</section>
<section class="section section--dark">
  <div class="container">
    <div class="section-head section-head--light reveal"><p class="eyebrow">{'Analiz Parametreleri' if tr else 'Test Parameters'}</p><h2>{'Neyi ölçüyoruz?' if tr else 'What we measure'}</h2></div>
    <div class="params">{pr}</div>
  </div>
</section>
{cta_band(lang)}"""
    body += footer(lang)
    return body

def page_about(lang):
    t = T[lang]; tr = lang == "tr"
    alt = url("about", "en" if tr else "tr")
    values = [("shield", "Dürüstlük", "Ürünü olduğu gibi anlatır, sözleşmeye harfiyen uyarız.", "Integrity", "We describe goods as they are and honour every contract term."),
              ("sparkle", "Kalite", "Kaliteyi bir etiket değil, her partide tekrarlanan bir disiplin olarak görürüz.", "Quality", "Quality is a discipline repeated on every lot, not a label."),
              ("clock", "Zamanında teslim", "Sevkiyat takvimine bağlılık, alıcımızın üretim planına saygıdır.", "On-time delivery", "Keeping to schedule is respect for our buyers' production plans."),
              ("handshake", "Kalıcı ilişki", "Her müşteriyi uzun soluklu bir iş ortağı olarak görürüz.", "Lasting relationships", "We treat every customer as a long-term partner.")]
    vals = "".join(f'<div class="feature reveal"><div class="feature__icon">{icon(i, 26)}</div><h3>{a if tr else c}</h3><p>{b if tr else d}</p></div>' for i, a, b, c, d in values)
    body = head(lang, "Hakkımızda — Asya Çerez Dış Ticaret Ltd. Şti." if tr else "About Us — Asya Çerez Foreign Trade Ltd.",
                ("İstanbul Fatih merkezli Asya Çerez Dış Ticaret Limited Şirketi'nin hikâyesi, misyonu, vizyonu ve değerleri." if tr else
                 "The story, mission, vision and values of Asya Çerez Foreign Trade Ltd., based in Fatih, Istanbul."),
                url("about", lang), alt, og_img="/assets/img/market.webp", jsonld=[org_ld()])
    body += header(lang, "about", alt)
    body += page_hero(lang, t["nav_about"], ("Asya’dan Anadolu’ya, Anadolu’dan dünyaya" if tr else "From Asia to Anatolia, from Anatolia to the world"), "",
                      "market.webp", [(t["nav_home"], url("home", lang)), (t["nav_about"], None)])
    body += f"""
<section class="section">
  <div class="container split">
    <div class="split__text reveal">
      <p class="eyebrow">{'Hikâyemiz' if tr else 'Our Story'}</p>
      <h2>{'Tarihi İpek Yolu’nun ticaret geleneğinden ilham alıyoruz' if tr else 'Inspired by the trading tradition of the Silk Road'}</h2>
      <p>{"Yüzyıllar boyunca baharat, kuru meyve ve kuruyemiş kervanları Asya'dan Anadolu'ya, oradan da dünyaya ulaştı. İstanbul'un tarihi yarımadasında, bu ticaretin kalbinin attığı Fatih'te kurulan Asya Çerez, adını ve ruhunu bu köklü gelenekten alıyor." if tr else "For centuries, caravans carried spices, dried fruits and nuts from Asia to Anatolia and on to the world. Founded in Fatih — at the heart of that trade on Istanbul's historic peninsula — Asya Çerez takes its name and spirit from this deep-rooted tradition."}</p>
      <p>{"Bugün aynı yolu modern dış ticaretin araçlarıyla yürüyoruz: Türkiye'nin dünyaya kazandırdığı fındık, Antep fıstığı, kayısı, incir ve üzümü uluslararası alıcılarla buluşturuyor; kaju, badem, ceviz ve hurma gibi ürünleri de dünyanın en iyi üretim bölgelerinden tedarik ediyoruz. Amacımız; kaliteyi, şeffaflığı ve zamanında teslimatı her siparişte standart hale getirmek." if tr else "Today we walk the same road with the tools of modern trade: connecting Türkiye's hazelnuts, pistachios, apricots, figs and raisins with international buyers, and sourcing cashews, almonds, walnuts and dates from the world's best growing regions. Our goal is to make quality, transparency and on-time delivery standard on every order."}</p>
    </div>
    <div class="split__media reveal"><img class="split__img1" src="/assets/img/market-2.webp" alt="" loading="lazy"><img class="split__img2" src="/assets/img/products/kuru-kayisi-1-sm.webp" alt="" loading="lazy"></div>
  </div>
</section>
<section class="section section--cream">
  <div class="container two-col two-col--cards">
    <div class="card card--mv reveal"><p class="eyebrow">{'Misyonumuz' if tr else 'Our Mission'}</p><h3>{'Doğru ürünü, doğru kalitede, doğru zamanda ulaştırmak.' if tr else 'The right product, at the right quality, at the right time.'}</h3>
      <p>{'Alıcılarımızın şartnamesine tam uyan ürünleri, rekabetçi fiyat ve güvenilir lojistikle teslim ederek onların işini kolaylaştırmak.' if tr else "Making our buyers' business easier by delivering products that meet their specification exactly, with competitive pricing and reliable logistics."}</p></div>
    <div class="card card--mv reveal"><p class="eyebrow">{'Vizyonumuz' if tr else 'Our Vision'}</p><h3>{'Türk kuruyemişinin dünyadaki güvenilir adresi olmak.' if tr else 'To be the trusted global name for Turkish nuts and dried fruits.'}</h3>
      <p>{'Kalite ve dürüstlükle anılan, birçok ülkede kalıcı iş ortaklıkları kurmuş bir dış ticaret markası olmak.' if tr else 'A trade brand known for quality and integrity, with lasting partnerships in many countries.'}</p></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">{'Değerlerimiz' if tr else 'Our Values'}</p><h2>{'Bizi biz yapan ilkeler' if tr else 'The principles that define us'}</h2></div>
    <div class="features features--4 features--light">{vals}</div>
  </div>
</section>
<section class="section section--cream section--tight">
  <div class="container">
    <div class="company reveal">
      <img src="/assets/brand/logo-full.svg" alt="Asya Çerez" width="170" height="221" loading="lazy">
      <dl>
        <div><dt>{'Ticari Unvan' if tr else 'Legal Name'}</dt><dd>{CO['legal']}</dd></div>
        <div><dt>{'Merkez Adres' if tr else 'Head Office'}</dt><dd>{e(CO['street'])}, {CO['district']} / {CO['city']} — {CO['country'][lang]}</dd></div>
        <div><dt>{'Faaliyet Alanı' if tr else 'Business'}</dt><dd>{'Kuruyemiş, çekirdek ve kuru meyve ithalatı, ihracatı ve toptan ticareti' if tr else 'Import, export and wholesale of nuts, seeds and dried fruits'}</dd></div>
        <div><dt>{t['email']}</dt><dd><a href="mailto:{CO['email']}">{CO['email']}</a></dd></div>
      </dl>
    </div>
  </div>
</section>
{cta_band(lang)}"""
    body += footer(lang)
    return body

def page_contact(lang):
    t = T[lang]; tr = lang == "tr"
    alt = url("contact", "en" if tr else "tr")
    opts = "".join(f'<option value="{p["slug"]}">{e(p["name"][lang])}</option>' for p in PRODUCTS)
    body = head(lang, "İletişim ve Teklif Formu" if tr else "Contact & Quotation Request",
                ("Asya Çerez ile iletişime geçin: fiyat teklifi, numune talebi ve iş birliği için formu doldurun. Adres: Mimar Kemalettin Mah., Fatih / İstanbul." if tr else
                 "Contact Asya Çerez for quotations, samples and partnerships. Address: Mimar Kemalettin, Fatih, Istanbul, Türkiye."),
                url("contact", lang), alt, og_img="/assets/img/ship-aerial.webp", jsonld=[org_ld()])
    body += header(lang, "contact", alt)
    body += page_hero(lang, t["nav_contact"], ("Birlikte çalışalım" if tr else "Let’s work together"),
                      ("Fiyat teklifi, numune veya iş birliği için formu doldurun; en kısa sürede dönüş yapalım." if tr else "Fill in the form for a quotation, samples or partnership — we'll reply promptly."),
                      "ship-aerial.webp", [(t["nav_home"], url("home", lang)), (t["nav_contact"], None)])
    phone_card = (f'<a class="ccard" href="tel:{CO["phone"].replace(" ", "")}">{icon("phone", 24)}<span><small>{t["phone"]}</small>{CO["phone"]}</span></a>' if CO["phone"] else "")
    wa_card = (f'<a class="ccard" href="https://wa.me/{CO["whatsapp"]}" target="_blank" rel="noopener">{icon("wa", 24)}<span><small>WhatsApp</small>{"Hemen yazın" if tr else "Message us"}</span></a>' if CO["whatsapp"] else "")
    L = (lambda a, b: a if tr else b)
    body += f"""
<section class="section">
  <div class="container contact">
    <div class="contact__info reveal">
      <p class="eyebrow">{L('İletişim Bilgileri','Contact Details')}</p>
      <h2>{CO['legal']}</h2>
      <div class="ccards">
        <div class="ccard">{icon('pin', 24)}<span><small>{t['address']}</small>{e(CO['street'])}<br>{CO['district']} / {CO['city']} — {CO['country'][lang]}</span></div>
        <a class="ccard" href="mailto:{CO['email']}">{icon('mail', 24)}<span><small>{t['email']}</small>{CO['email']}</span></a>
        {phone_card}{wa_card}
        <div class="ccard">{icon('clock', 24)}<span><small>{L('Çalışma Saatleri','Office Hours')}</small>{L('Pazartesi – Cumartesi · 09:00 – 18:00','Monday – Saturday · 09:00 – 18:00 (GMT+3)')}</span></div>
      </div>
      <div class="map"><iframe title="{L('Harita','Map')}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        src="https://maps.google.com/maps?q={html.escape(MAPS_Q).replace(' ', '+')}&z=16&output=embed&hl={lang}"></iframe></div>
    </div>
    <form class="qform reveal" id="quote-form" data-endpoint="{'https://api.web3forms.com/submit' if CO['form_key'] else CO['form_endpoint']}" data-key="{CO['form_key']}" data-email="{CO['email']}" data-lang="{lang}" novalidate>
      <h2>{L('Teklif & Numune Talebi','Quotation & Sample Request')}</h2>
      <p class="muted">{L('Satışlarımız yalnızca toptandır. Yıldızlı alanlar zorunludur.','We sell wholesale only. Fields marked * are required.')}</p>
      <div class="frow">
        <label>{L('Ad Soyad','Full name')} *<input name="name" required autocomplete="name"></label>
        <label>{L('Firma','Company')}<input name="company" autocomplete="organization"></label>
      </div>
      <div class="frow">
        <label>{t['email']} *<input name="email" type="email" required autocomplete="email"></label>
        <label>{t['phone']}<input name="phone" type="tel" autocomplete="tel"></label>
      </div>
      <div class="frow">
        <label>{L('Ülke','Country')}<input name="country" autocomplete="country-name"></label>
        <label>{L('Talep türü','Request type')}<select name="type">
          <option>{L('Fiyat teklifi','Price quotation')}</option><option>{L('Numune talebi','Sample request')}</option>
          <option>{L('İthalat talebi','Import enquiry')}</option><option>{L('İhracat talebi','Export enquiry')}</option><option>{L('Tedarikçi / iş birliği','Supplier / partnership')}</option><option>{L('Diğer','Other')}</option></select></label>
      </div>
      <div class="frow">
        <label>{L('Ürün','Product')}<select name="product"><option value="">{L('Seçiniz','Select')}</option>{opts}<option value="diger">{L('Diğer','Other')}</option></select></label>
        <label>{L('Tahmini miktar','Estimated quantity')}<input name="qty" placeholder="{L('örn. 1 × 20’ konteyner / 5 ton','e.g. 1 × 20’ container / 5 tons')}"></label>
      </div>
      <label>{L('Mesajınız','Message')} *<textarea name="message" rows="5" required placeholder="{L('Kalibre, ambalaj, teslim şekli (FOB, CIF…) ve varış noktası gibi detayları yazabilirsiniz.','Grade, packaging, delivery term (FOB, CIF…) and destination, etc.')}"></textarea></label>
      <label class="consent"><input type="checkbox" name="kvkk" required> <span>{L('Kişisel verilerimin, talebime yanıt verilmesi amacıyla işlenmesini kabul ediyorum (KVKK).','I agree that my personal data may be processed to respond to my request.')}</span></label>
      <button class="btn btn--gold btn--block" type="submit">{L('Talebi Gönder','Send Request')} {icon('arrow', 18)}</button>
      <p class="qform__status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>"""
    body += footer(lang)
    return body

def page_404():
    body = head("tr", "Sayfa bulunamadı", "Aradığınız sayfa bulunamadı.", "/404.html", "/404.html", noindex=True)
    body += header("tr", "", "/en/")
    body += f"""<section class="section notfound"><div class="container center">
      <img src="/assets/brand/logo-badge.svg" alt="" width="120" height="120">
      <h1>404</h1><p>Aradığınız sayfa bulunamadı. · The page you are looking for could not be found.</p>
      <div class="btn-row btn-row--center"><a class="btn btn--gold" href="/">Ana Sayfa</a><a class="btn btn--outline" href="/urunler/">Ürünler</a><a class="btn btn--outline" href="/en/">English</a></div>
    </div></section>"""
    body += footer("tr")
    return body

# ================================================================= ÇIKTI
def write(path, content):
    fp = os.path.join(OUT, path.lstrip("/"))
    if fp.endswith("/"): fp += "index.html"
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f: f.write(content)

def main():
    global PAGE_KEY
    for d in ["urunler", "en", "ar", "dis-ticaret", "kalite", "hakkimizda", "iletisim"]:
        shutil.rmtree(os.path.join(OUT, d), ignore_errors=True)
    urls = []
    post = lambda lang, h: arabize(h) if lang == "ar" else h
    for lang in LANGS:
        pages = {"home": page_home, "products": page_products, "trade": page_trade, "quality": page_quality, "about": page_about, "contact": page_contact}
        for k, fn in pages.items():
            PAGE_KEY = k
            write(url(k, lang), post(lang, fn(lang))); urls.append(url(k, lang))
        for p in PRODUCTS:
            PAGE_KEY = "product:" + p["slug"]
            write(product_url(p, lang), post(lang, page_product(p, lang))); urls.append(product_url(p, lang))
    PAGE_KEY = "home"
    write("/404.html", page_404())
    today = datetime.date.today().isoformat()
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    write("/sitemap.xml", sm)
    write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    write("/CNAME", "asyacerez.com\n")
    print(f"{len(urls)} sayfa üretildi → {OUT}")

if __name__ == "__main__":
    main()
