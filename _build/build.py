#!/usr/bin/env python3
"""Builds the Manifest Metals website.

Run from the repo root:  python3 _build/build.py
Every page is generated in English and Spanish into the repo root, which
GitHub Pages serves as-is.

Copy rules
- No prices. No license, insurance, bonding, warranty or review claims until verified.
- Texas only. Energy claims cite the EPA peak-cooling figure only.
- Colors: only the 12 on the current chart (never "Bronze").
- Project write-ups never publish a customer's name or street address.
- Diagrams and the color visualizer are illustrations; project photos are real Manifest jobs.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from art import FOOTER_RIDGE, icon, r_panel_profile, standing_seam_profile  # noqa: E402
from logo import emblem  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_URL = "https://manifestmetals.com"
PHONE = "(915) 861-6436"
TEL = "+19158616436"
EMAIL = "manifestmetalsep@gmail.com"
# Quote form posts here. FormSubmit emails EMAIL a one-time activation link on the first submission.
FORM_ENDPOINT = f"https://formsubmit.co/ajax/{EMAIL}"
EPA_URL = "https://www.epa.gov/heatislands/using-cool-roofs-reduce-heat-islands"

PAGES = {
    "home": {"en": "", "es": "es/"},
    "residential": {"en": "residential/", "es": "es/residencial/"},
    "commercial": {"en": "commercial/", "es": "es/comercial/"},
    "projects": {"en": "projects/", "es": "es/proyectos/"},
    "shingle": {"en": "shingle-to-metal/", "es": "es/de-tejas-a-metal/"},
    "guide": {"en": "standing-seam-vs-r-panel/", "es": "es/standing-seam-vs-r-panel/"},
    "about": {"en": "about/", "es": "es/nosotros/"},
    "contact": {"en": "contact/", "es": "es/contacto/"},
    "privacy": {"en": "privacy/", "es": "es/privacidad/"},
}

AREAS = ["El Paso", "Horizon City", "Socorro", "San Elizario", "Clint", "Fabens", "Canutillo", "Vinton", "Anthony, TX"]

# Real job photos live in assets/img/p/, illustrations in assets/img/r/
IMAGES = {}
for n in range(1, 6):
    IMAGES[f"job{n}"] = (800, 1280)   # Houston area, standing seam
    IMAGES[f"gv{n}"] = (800, 1600)    # Galveston, standing seam
for n in range(1, 4):
    IMAGES[f"el{n}"] = (800, 1600)    # El Paso, shingle-to-metal (R-panel)

# The 12 colors on the current 26 ga chart (swatch hex values are approximate)
COLORS = [
    ("light-stone", "Light Stone", "Light Stone", "#d6cfbb"),
    ("polar-white", "Polar White", "Polar White", "#eeeee9"),
    ("saddle-tan", "Saddle Tan", "Saddle Tan", "#a88b67"),
    ("burnished-slate", "Burnished Slate", "Burnished Slate", "#5d5246"),
    ("koko-brown", "Koko Brown", "Koko Brown", "#4a3a2d"),
    ("black", "Black", "Negro", "#1e1f21"),
    ("charcoal-gray", "Charcoal Gray", "Charcoal Gray", "#4b4e52"),
    ("rustic-red", "Rustic Red", "Rustic Red", "#7d2e24"),
    ("evergreen", "Evergreen", "Evergreen", "#2e4a3b"),
    ("hawaiian-blue", "Hawaiian Blue", "Hawaiian Blue", "#33709e"),
    ("galvalume", "Acrylic Galvalume", "Galvalume acrílico", "#c3c7cb"),
    ("copper-metallic", "Copper Metallic", "Cobre metálico", "#a4683f"),
]
for key, *_ in COLORS:
    IMAGES["k-" + key] = (800, 1600)

LANG = "en"
CURRENT = "home"


def tr(en, es):
    return en if LANG == "en" else es


def url(key, lang=None, anchor=""):
    """Relative link from the current page to another page."""
    lang = lang or LANG
    rel = "../" * PAGES[CURRENT][LANG].count("/") + PAGES[key][lang]
    return (rel or "./") + anchor


def asset(path):
    return "../" * PAGES[CURRENT][LANG].count("/") + "assets/" + path


def img_path(name, w):
    return f"img/{'p' if name.startswith(('job', 'el', 'gv')) else 'r'}/{name}-{w}.webp"


def srcset(name):
    return ", ".join(f"{asset(img_path(name, w))} {w}w" for w in IMAGES[name])


def img(name, alt, sizes="100vw", cls="", eager=False):
    mid = IMAGES[name][1]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{asset(img_path(name, mid))}" srcset="{srcset(name)}" sizes="{sizes}" '
            f'width="{mid}" height="{int(mid * 9 / 16)}" alt="{alt}" {load}>')


def tel_btn(cls="btn", label=None):
    return f'<a class="{cls}" href="tel:{TEL}">{icon("phone")}{label or PHONE}</a>'


def quote_btn(cls="btn btn-lg"):
    return f'<a class="{cls}" href="{url("contact", anchor="#quote")}">{tr("Request a quote", "Pida una cotización")}</a>'


def brand(size=""):
    return (f'<span class="brand-mark{size}">{emblem("logo-svg", "")}</span>'
            '<span class="brand-text"><span class="brand-name">Manifest</span><span class="brand-sub">Metals</span></span>')


def epa(text):
    return f'<a href="{EPA_URL}" rel="noopener">{text}</a>'


def points(items):
    return "".join(f'<li><span class="ic">{icon(i)}</span><div><strong>{t}</strong><p>{d}</p></div></li>' for i, t, d in items)


def cards(items):
    return "".join(f'<div class="card reveal"><div class="ic">{icon(i)}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in items)


# ---------------------------------------------------------------- layout

def head(title, desc, image="el3", extra_ld=None, crumb=None):
    here = PAGES[CURRENT]
    canonical = SITE_URL + "/" + here[LANG]
    alt = "".join(
        f'<link rel="alternate" hreflang="{lg}" href="{SITE_URL}/{here[lg]}">' for lg in ("en", "es")
    ) + f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}/{here["en"]}">'
    ld = [{
        "@context": "https://schema.org",
        "@type": "RoofingContractor",
        "@id": SITE_URL + "/#business",
        "name": "Manifest Metals, LLC",
        "url": SITE_URL + "/",
        "logo": SITE_URL + "/assets/img/logo.png",
        "image": SITE_URL + "/assets/img/og.jpg",
        "telephone": "+1-915-861-6436",
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": "El Paso", "addressRegion": "TX", "addressCountry": "US"},
        "areaServed": [{"@type": "AdministrativeArea", "name": "El Paso County, Texas"}]
                      + [{"@type": "City", "name": a.replace(", TX", "")} for a in AREAS],
        "knowsLanguage": ["en", "es"],
        "description": desc,
    }]
    if crumb:
        ld.append({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": tr("Home", "Inicio"), "item": f"{SITE_URL}/{PAGES['home'][LANG]}"},
                {"@type": "ListItem", "position": 2, "name": crumb, "item": canonical},
            ],
        })
    ld.extend(extra_ld or [])
    preload = ""
    if image:
        preload = (f'<link rel="preload" as="image" href="{asset(img_path(image, IMAGES[image][1]))}" '
                   f'imagesrcset="{srcset(image)}" imagesizes="100vw">')
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f'''<!DOCTYPE html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{alt}
<meta name="theme-color" content="#161412">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Manifest Metals">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/assets/img/og.jpg">
<meta property="og:locale" content="{tr('en_US', 'es_MX')}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{asset('img/favicon.svg')}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{asset('img/apple-touch-icon.png')}">
<link rel="preload" href="{asset('fonts/archivo.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{asset('fonts/inter.woff2')}" as="font" type="font/woff2" crossorigin>
{preload}
<link rel="stylesheet" href="{asset('css/site.css')}">
{lds}
</head>
<body>
<a class="skip-link" href="#main">{tr('Skip to content', 'Ir al contenido')}</a>
'''


NAV = [
    ("residential", ("Residential", "Residencial")),
    ("commercial", ("Commercial", "Comercial")),
    ("projects", ("Our Work", "Proyectos")),
    ("shingle", ("Shingle to Metal", "De tejas a metal")),
    ("about", ("About", "Nosotros")),
    ("contact", ("Contact", "Contacto")),
]


def header():
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{url(k)}"{cur if k == CURRENT else ""}>{tr(*lbl)}</a>' for k, lbl in NAV)
    other = "es" if LANG == "en" else "en"
    return f'''<aside class="topbar" aria-label="{tr('Quick contact', 'Contacto rápido')}"><div class="container">
  <ul><li lang="es">Se habla español</li><li>{tr('Locally owned', 'Negocio local')}</li><li>{tr('El Paso County, Texas', 'Condado de El Paso, Texas')}</li></ul>
  <a href="tel:{TEL}">{PHONE}</a>
</div></aside>
<header class="site-header">
  <div class="container">
    <a class="brand" href="{url('home')}" aria-label="Manifest Metals — {tr('home', 'inicio')}">{brand()}</a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="{tr('Menu', 'Menú')}"><span></span><span></span><span></span></button>
    <nav class="nav" id="site-nav" aria-label="{tr('Main', 'Principal')}">
      {links}
      <a class="lang" href="{url(CURRENT, other)}" lang="{other}" hreflang="{other}">{tr('Español', 'English')}</a>
      {tel_btn()}
    </nav>
  </div>
</header>
<main id="main">
'''


def cta_band():
    return f'''<section class="cta-band">
  <div class="container">
    <div>
      <h2>{tr("Let's talk about your roof.", "Hablemos de su techo.")}</h2>
      <p>{tr("Call us, or send a few details and we'll get back to you.", "Llámenos, o envíenos algunos datos y nos comunicamos con usted.")} <span lang="es">Se habla español.</span></p>
    </div>
    <div class="actions">
      {tel_btn("btn btn-lg")}
      {quote_btn("btn btn-lg btn-ghost")}
    </div>
  </div>
</section>
'''


def footer(ridge_on="on-brand"):
    def col(title, rows):
        return f'<div><h2 class="foot-h">{title}</h2><ul>{"".join(rows)}</ul></div>'

    def li(k, label):
        return f'<li><a href="{url(k)}">{label}</a></li>'
    other = "es" if LANG == "en" else "en"
    return f'''</main>
<footer class="site-footer">
  {FOOTER_RIDGE.format(cls=ridge_on)}
  <div class="container">
    <div class="footer-top">
      <div>
        <a class="brand" href="{url('home')}" aria-label="Manifest Metals">{brand(" lg")}</a>
        <p class="footer-blurb">{tr("Metal roofing and siding for homes and commercial buildings. Standing seam, R-panel and metal wall panels — based in El Paso, Texas.", "Techos y revestimiento de metal para casas y edificios comerciales. Standing seam, R-panel y paneles de pared — con base en El Paso, Texas.")}</p>
      </div>
      {col(tr('Services', 'Servicios'), [li('residential', tr('Residential roofing', 'Techos residenciales')), li('shingle', tr('Shingle to metal', 'De tejas a metal')), li('commercial', tr('Commercial & wall panels', 'Comercial y paneles de pared')), li('guide', 'Standing seam vs R-panel')])}
      {col(tr('Company', 'Empresa'), [li('projects', tr('Our work', 'Proyectos')), li('about', tr('About us', 'Nosotros')), li('contact', tr('Contact', 'Contacto')), f'<li><a href="{url(CURRENT, other)}" lang="{other}">{tr("Español", "English")}</a></li>'])}
      <div>
        <h2 class="foot-h">{tr('Call us', 'Llámenos')}</h2>
        <ul>
          <li><a class="footer-phone" href="tel:{TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{tr('El Paso County, Texas', 'Condado de El Paso, Texas')}</li>
          <li lang="es">Se habla español</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span id="year">2026</span> Manifest Metals, LLC</span>
      <span>{tr('Project photos are our work. Diagrams and the color visualizer are illustrations.', 'Las fotos de proyectos son de nuestro trabajo. Los diagramas y el visualizador son ilustraciones.')} <a href="{url('privacy')}">{tr('Privacy', 'Privacidad')}</a></span>
    </div>
  </div>
</footer>
<nav class="callbar" aria-label="{tr('Call or get a quote', 'Llamar o cotizar')}">
  {tel_btn("btn", tr("Call now", "Llamar"))}
  <a class="btn btn-ghost" href="{url('contact', anchor='#quote')}">{tr('Get a quote', 'Cotizar')}</a>
</nav>
<dialog class="lightbox" aria-label="{tr('Photo', 'Foto')}"><button type="button" class="lb-close" aria-label="{tr('Close', 'Cerrar')}">×</button><img alt=""></dialog>
<script src="{asset('js/site.js')}" defer></script>
</body>
</html>
'''


def photo_hero(image, alt, crumb, title, lead, actions=True, pos=None):
    crumbs = (f'<nav class="crumbs" aria-label="{tr("Breadcrumb", "Ruta")}"><a href="{url("home")}">{tr("Home", "Inicio")}</a>'
              f'<span aria-hidden="true">/</span>{crumb}</nav>') if crumb else ""
    btns = f'<div class="hero-cta">{quote_btn()}{tel_btn("btn btn-lg btn-ghost")}</div>' if actions else ""
    style = f' style="--pos:{pos}"' if pos else ""
    return f'''<section class="photo-hero dark"{style}>
  <div class="photo-hero-img">{img(image, alt, eager=True)}</div>
  <div class="container">
    {crumbs}
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
    {btns}
  </div>
</section>
'''


def faq_block(items, bg=""):
    rows = "".join(f'<details><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>' for q, a in items)
    return f'''<section class="section {bg}">
  <div class="container faq-wrap">
    <div class="section-head">
      <p class="eyebrow">FAQ</p>
      <h2>{tr('Common questions', 'Preguntas frecuentes')}</h2>
      <p>{tr("Don't see yours? Call us — we're happy to talk it through.", "¿No encuentra la suya? Llámenos, con gusto le explicamos.")}</p>
    </div>
    <div class="faq reveal">{rows}</div>
  </div>
</section>
'''


def faq_ld(items):
    def strip(t):
        return re.sub(r"<[^>]+>", "", t).replace("&quot;", '"')
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}


def process(bg=""):
    steps = [
        (tr("Call or send a request", "Llame o envíe su solicitud"),
         tr("Tell us about the building and what you have in mind — new roof, conversion, siding or a repair.", "Cuéntenos sobre la propiedad y lo que tiene en mente — techo nuevo, cambio de tejas a metal, revestimiento o reparación.")),
        (tr("We inspect & photograph", "Inspeccionamos y fotografiamos"),
         tr("An aerial measurement report, then a site visit with a checklist built for your roof type. Photos come before any price.", "Un reporte de medidas aéreo y luego una visita con una lista de revisión hecha para su tipo de techo. Primero las fotos, después el precio.")),
        (tr("Written quote", "Cotización por escrito"),
         tr("Priced at the office, never guessed on the roof — with the system, color and scope spelled out.", "Se calcula en la oficina, nunca se adivina en el techo — con el sistema, el color y el alcance por escrito.")),
        (tr("Installed & cleaned up", "Instalación y limpieza"),
         tr("Daily cleanup, a magnet sweep of the yard and a final walk of the roof with you.", "Limpieza diaria, barrido con imán del patio y un recorrido final del techo con usted.")),
    ]
    items = "".join(f'<li class="step reveal"><h3>{t}</h3><p>{d}</p></li>' for t, d in steps)
    return f'''<section class="section {bg}">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">{tr('How it works', 'Cómo funciona')}</p>
      <h2>{tr('From first call to final walk-through', 'De la primera llamada al recorrido final')}</h2>
    </div>
    <ol class="steps">{items}</ol>
  </div>
</section>
'''


def lifespan_chart():
    rows = [
        (tr("Standing seam, 24 ga steel", "Standing seam, acero calibre 24"), tr("40–70 yrs", "40–70 años"), 40, 70, ""),
        (tr("Asphalt shingles, in our sun", "Tejas de asfalto, con nuestro sol"), tr("often 15–20", "con frecuencia 15–20"), 15, 20, "muted"),
        (tr("Screw washers on exposed-fastener panels", "Arandelas de tornillos en paneles expuestos"), tr("can start failing 10–15", "pueden fallar a los 10–15"), 10, 15, "warn"),
    ]
    bars = "".join(
        f'''<div class="bar-row"><div class="bar-label"><span>{name}</span><span>{val}</span></div>
        <div class="bar-track"><div class="bar-fill {cls}" style="left:{lo / 70 * 100:.2f}%;width:{(hi - lo) / 70 * 100:.2f}%"></div></div></div>'''
        for name, val, lo, hi, cls in rows
    )
    axis = "".join(f"<span>{n}</span>" for n in range(0, 71, 10))
    return f'''<div class="chart-card reveal">
  <h3>{tr('Typical service life', 'Vida útil típica')}</h3>
  <p class="sub">{tr('Years. In our sun, how a roof is fastened matters as much as the metal.', 'Años. Con nuestro sol, cómo se fija el techo importa tanto como el metal.')}</p>
  <div class="bars">{bars}</div>
  <div class="bar-axis" aria-hidden="true">{axis}</div>
  <p class="chart-note">{tr('Typical industry ranges, not a warranty. Washers are a maintenance item — an R-panel roof itself lasts decades when its fasteners are kept up. Actual life depends on the product, finish and installation.', 'Rangos típicos de la industria, no una garantía. Las arandelas son mantenimiento — un techo R-panel dura décadas si se cuidan sus tornillos. La vida real depende del producto, el acabado y la instalación.')}</p>
</div>'''


def systems(links=True, homes=True):
    ss_link = f'<a class="link-arrow" href="{url("guide")}">Standing seam vs R-panel</a>' if links else ""
    rp_link = f'<a class="link-arrow" href="{url("guide")}">{tr("Compare the two", "Compare los dos")}</a>' if links else ""
    return f'''<div class="systems">
  <article class="system reveal">
    <div class="system-photo">{img("job2", tr("Standing seam metal roof panels meeting at a ridge, project photo", "Paneles standing seam que se unen en una cumbrera, foto de proyecto"), "(max-width: 960px) 100vw, 600px")}</div>
    <div class="system-body">
      <span class="tag">{tr('Our recommendation for homes', 'Nuestra recomendación para casas') if homes else tr('Concealed fastener', 'Fijación oculta')}</span>
      <h3>Standing seam</h3>
      <dl class="specs"><div><dt>{tr('Steel', 'Acero')}</dt><dd>24 ga</dd></div><div><dt>{tr('Seam', 'Costura')}</dt><dd>1-3/4&quot; snap-lock</dd></div><div><dt>{tr('Panel', 'Panel')}</dt><dd>{tr('18&quot; wide', '18&quot; de ancho')}</dd></div></dl>
      <ul class="checks">
        <li>{tr('Concealed clips — no screws through the panel face', 'Clips ocultos — sin tornillos en la cara del panel')}</li>
        <li>{tr('Striated pans that hide oil-canning on the flat of the panel', 'Paneles estriados que disimulan las ondulaciones en la parte plana')}</li>
        <li>{tr('40–70 year typical service life (industry range)', 'Vida útil típica de 40 a 70 años (rango de la industria)')}</li>
      </ul>
      {ss_link}
    </div>
  </article>
  <article class="system reveal">
    <div class="system-photo">{img("el3", tr("Light Stone R-panel roof on an El Paso home, project photo", "Techo R-panel color Light Stone en una casa de El Paso, foto de proyecto"), "(max-width: 960px) 100vw, 600px")}</div>
    <div class="system-body">
      <span class="tag neutral">{tr('Strong & economical', 'Resistente y económico')}</span>
      <h3>R-panel</h3>
      <dl class="specs"><div><dt>{tr('Steel', 'Acero')}</dt><dd>26 ga</dd></div><div><dt>{tr('Coverage', 'Cobertura')}</dt><dd>{tr('36&quot; per panel', '36&quot; por panel')}</dd></div><div><dt>{tr('Colors', 'Colores')}</dt><dd>{tr('12 on the chart', '12 en la carta')}</dd></div></dl>
      <ul class="checks">
        <li>{tr('Ribbed exposed-fastener panel — strong and economical', 'Panel acanalado con tornillos expuestos — resistente y económico')}</li>
        <li>{tr('A great fit for homes, shops, barns and commercial', 'Ideal para casas, talleres, graneros y obras comerciales')}</li>
        <li>{tr('Plan on checking fasteners as the roof ages', 'Conviene revisar los tornillos con los años')}</li>
      </ul>
      {rp_link}
    </div>
  </article>
</div>
<p class="fine-center">{tr('Both systems need a roof pitch of at least 3:12. Flatter roofs need a different approach — ask us.', 'Ambos sistemas requieren una inclinación de al menos 3:12. Los techos más planos necesitan otra solución — pregúntenos.')}</p>'''


def visualizer():
    swatches = "".join(
        f'<button type="button" class="swatch{" active" if i == 0 else ""}" aria-pressed="{"true" if i == 0 else "false"}" '
        f'data-src="{asset(img_path("k-" + key, 1600))}" data-srcset="{srcset("k-" + key)}" data-name="{tr(en, es)}" data-value="{en}">'
        f'<span class="chip" style="--c:{hexc}"></span><span class="swatch-name">{tr(en, es)}'
        f'{"<small>Premium</small>" if key == "copper-metallic" else ""}</span></button>'
        for i, (key, en, es, hexc) in enumerate(COLORS)
    )
    k0, en0, es0, hex0 = COLORS[0]
    return f'''<section class="section visualizer-section" id="colors">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">{tr('Color visualizer', 'Visualizador de colores')}</p>
      <h2>{tr('See your roof in color.', 'Vea su techo a color.')}</h2>
      <p>{tr('Tap a color to see it on an R-panel roof — all 12 colors on our chart. Lighter colors reflect more of our sun.', 'Toque un color para verlo en un techo R-panel — los 12 colores de nuestra carta. Los colores claros reflejan más el sol.')}</p>
    </div>
    <div class="viz reveal">
      <div class="viz-stage" aria-live="polite">
        {img("k-" + k0, tr("Illustration of a home with an R-panel roof in the selected color", "Ilustración de una casa con techo R-panel en el color seleccionado"), "(max-width: 1240px) 100vw, 1180px", cls="viz-img")}
        <span class="viz-label"><span class="chip" style="--c:{hex0}"></span><span class="viz-name">{tr(en0, es0)}</span></span>
      </div>
      <div class="swatches" role="group" aria-label="{tr('Roof colors', 'Colores de techo')}">{swatches}</div>
      <div class="viz-cta"><a class="btn" id="viz-quote" data-base="{url("contact")}" href="{url("contact")}?color={en0.replace(" ", "+")}#quote">{tr("Get a quote in", "Cotizar en")} <span class="viz-name-cta">{tr(en0, es0)}</span></a></div>
      <p class="viz-note">{tr('Illustration — screen colors are approximate. We bring physical color chips to your site visit. In-stock colors usually start sooner than special orders. Standing seam comes in its own premium color range — ask us.', 'Ilustración — los colores en pantalla son aproximados. Llevamos muestras físicas a la visita. Los colores en existencia normalmente empiezan antes que los pedidos especiales. El standing seam tiene su propia gama de colores — pregúntenos.')}</p>
    </div>
  </div>
</section>
'''


def insurance():
    return f'''<section class="section-tight">
  <div class="container">
    <div class="insure reveal">
      <div class="insure-law"><span class="mono">UL 2218</span><strong>{tr('Class 4', 'Clase 4')}</strong></div>
      <div>
        <p class="eyebrow">{tr('Hail & insurance', 'Granizo y seguro')}</p>
        <h2>{tr('An impact-rated roof may lower your insurance.', 'Un techo resistente al impacto podría bajar su seguro.')}</h2>
        <p>{tr("In Texas, home insurers offer discounts for eligible roofs rated UL 2218 Class 4 for impact resistance. Whether yours qualifies depends on the exact tested system, how it's installed and your policy — each insurer sets its own rules and amount.", "En Texas, las aseguradoras ofrecen descuentos para techos elegibles con clasificación UL 2218 Clase 4 de resistencia al impacto. Si el suyo califica depende del sistema probado, de cómo se instala y de su póliza — cada aseguradora fija sus reglas y su monto.")}</p>
        <p class="insure-ask">{tr('Confirm the system and requirements with your insurer before installation — we will give you the product details they ask for.', 'Confirme el sistema y los requisitos con su aseguradora antes de instalar — le damos los datos del producto que le pidan.')}</p>
      </div>
    </div>
  </div>
</section>
'''


def tiles(items, cls="ep-grid"):
    out = []
    for i, (name, cap, alt) in enumerate(items):
        big = " ep-big" if i == 0 else ""
        sizes = "(max-width: 960px) 100vw, 40vw" if i == 0 else "(max-width: 960px) 50vw, 25vw"
        out.append(f'<button type="button" class="g-tile{big}" data-full="{asset(img_path(name, IMAGES[name][-1]))}" '
                   f'aria-label="{tr("View photo", "Ver foto")}: {cap}">{img(name, alt, sizes)}<span class="g-cap mono">{cap}</span></button>')
    return f'<div class="{cls}">{"".join(out)}</div>'


def case(anchor, photos, eyebrow, title, facts, scope, extra="", link="", h="h3"):
    fact_html = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in facts)
    scope_html = "".join(f"<li>{x}</li>" for x in scope)
    return f'''<article class="case reveal" id="{anchor}">
  <div class="case-media">{tiles(photos)}</div>
  <div class="case-body">
    <p class="eyebrow">{eyebrow}</p>
    <{h} class="case-title">{title}</{h}>
    <dl class="facts-list">{fact_html}</dl>
    <ul class="checks">{scope_html}</ul>
    {extra}{link}
  </div>
</article>'''


# Project write-ups (never a customer's name or street address)
def project_elpaso(h="h3", compact=False):
    hs = "h" + str(int(h[1]) + 1)
    story = f'''<div class="story">
      <{hs}>{tr('The color decision', 'La decisión del color')}</{hs}>
      <p>{tr("The family weighed a special-order Hawaiian Blue against Light Stone, which was in stock. Same roof, same crew — the in-stock color let work start weeks sooner, and the light finish reflects more of the El Paso sun.", "La familia comparó un Hawaiian Blue de pedido especial con Light Stone, que estaba en existencia. Mismo techo, mismo equipo — el color en existencia permitió empezar semanas antes, y el acabado claro refleja más el sol de El Paso.")}</p>
    </div>'''
    return case(
        "el-paso",
        [("el3", "El Paso, TX", tr("Light Stone R-panel roof on an El Paso home, palm trees and the city behind", "Techo R-panel Light Stone en una casa de El Paso, con palmeras y la ciudad al fondo")),
         ("el1", tr("Cooler & vents", "Cooler y ventilas"), tr("Drone view of the new roof flashed around a swamp cooler and vents", "Vista con dron del techo nuevo con tapajuntas alrededor del cooler y las ventilas")),
         ("el2", tr("From above", "Desde arriba"), tr("Overhead view of the finished R-panel roof", "Vista aérea del techo R-panel terminado"))],
        tr("Shingle to metal · El Paso", "De tejas a metal · El Paso"),
        tr("From worn shingles to a 26-gauge metal roof.", "De tejas gastadas a un techo de metal calibre 26."),
        [(tr("Where", "Dónde"), "El Paso, TX"), (tr("System", "Sistema"), tr("26 ga R-panel", "R-panel calibre 26")),
         (tr("Color", "Color"), "Light Stone"), (tr("Size", "Tamaño"), tr("~2,600 sq ft", "~2,600 pies²"))],
        [tr("Old shingles torn off down to the bare wood deck and hauled away", "Tejas viejas retiradas hasta la cubierta de madera y desechadas"),
         tr("Entire roof covered in self-sealing waterproof membrane before any metal", "Todo el techo cubierto con membrana impermeable autoadherible antes del metal"),
         tr("R-panel over the main house, front porch and entry", "R-panel en la casa, el porche y la entrada"),
         tr("Color-matched ridge caps, rake and edge trim, sidewall and transition flashing", "Cumbreras, remates y tapajuntas del mismo color"),
         tr("New seals on all 8 pipes and vents, plus a new 12&quot; turbine vent", "Sellos nuevos en los 8 tubos y ventilas, y una turbina nueva de 12&quot;"),
         tr("Permit, daily cleanup, a magnet sweep of the yard and a final walk with the family", "Permiso, limpieza diaria, barrido con imán y recorrido final con la familia")][::2 if compact else 1],
        extra="" if compact else story, h=h,
        link=f'<a class="link-arrow" href="{url("projects", anchor="#el-paso")}">{tr("The full project", "El proyecto completo")}</a>' if compact else "",
    )


def project_galveston(h="h3"):
    return case(
        "galveston",
        [("gv1", tr("Beachfront · Galveston", "Frente al mar · Galveston"), tr("Crew installing standing seam panels on a beachfront home, the Gulf of Mexico behind", "Equipo instalando paneles standing seam en una casa frente al mar, con el Golfo de México al fondo")),
         ("gv3", tr("Tied off, every hip", "Asegurados en cada limatesa"), tr("Crew in fall protection on a multi-hip standing seam roof", "Equipo con protección contra caídas en un techo standing seam de varias limatesas")),
         ("gv4", tr("Cupola flashing", "Tapajuntas de cúpula"), tr("Standing seam flashing around a cupola", "Tapajuntas standing seam alrededor de una cúpula"))],
        tr("Standing seam · Galveston", "Standing seam · Galveston"),
        tr("A beachfront roof on the Gulf.", "Un techo frente al Golfo."),
        [(tr("Where", "Dónde"), "Galveston, TX"), (tr("System", "Sistema"), "Standing seam"),
         (tr("Details", "Detalles"), tr("Hips, valleys, skylight, cupola", "Limatesas, limahoyas, tragaluz, cúpula"))],
        [tr("Multi-hip roof with valleys, a skylight and a cupola — every transition flashed", "Techo de varias limatesas con limahoyas, tragaluz y cúpula — cada transición con tapajuntas"),
         tr("Installed over synthetic underlayment, steps from the surf", "Instalado sobre membrana sintética, a unos pasos del mar"),
         tr("Crew in harnesses and tied off on every slope", "Equipo con arnés y asegurado en cada pendiente")],
        h=h,
    )


def project_houston(h="h3"):
    return case(
        "houston",
        [("job3", tr("Houston area", "Área de Houston"), tr("Dark standing seam metal roof under a cloudy sky", "Techo standing seam oscuro bajo un cielo con nubes")),
         ("job4", tr("Hips & valleys", "Limatesas y limahoyas"), tr("Standing seam hips and valleys during installation", "Limatesas y limahoyas standing seam durante la instalación")),
         ("job1", tr("From above", "Desde arriba"), tr("Overhead drone view of a large standing seam roof", "Vista aérea con dron de un techo standing seam grande"))],
        tr("Standing seam · Houston area", "Standing seam · Área de Houston"),
        tr("A cut-up roofline on new construction.", "Un techo complejo en construcción nueva."),
        [(tr("Where", "Dónde"), tr("Houston area, TX", "Área de Houston, TX")), (tr("System", "Sistema"), "Standing seam"),
         (tr("Details", "Detalles"), tr("Dozens of hips & valleys", "Decenas de limatesas y limahoyas"))],
        [tr("A large new home with a heavily cut-up hip roof", "Una casa nueva grande con un techo de muchas limatesas"),
         tr("Panels cut to fit every hip and valley", "Paneles cortados para cada limatesa y limahoya"),
         tr("Color-matched hip caps, ridge and valley trim", "Limatesas, cumbreras y limahoyas del mismo color")],
        h=h,
    )


def inspection(bg="bone"):
    types = [
        ("roof", tr("Shingle roofs", "Techos de tejas"), tr("A 10' × 10' hail test square on every slope, plus vents and soft metals — what an adjuster checks.", "Un cuadro de prueba de granizo de 10' × 10' en cada pendiente, más ventilas y metales — lo que revisa un ajustador.")),
        ("home", tr("Tile roofs", "Techos de teja de barro"), tr("On tile, the underlayment is the real roof. We lift tile in at least two places and record what's under it.", "En la teja, la membrana es el verdadero techo. Levantamos tejas en al menos dos lugares y registramos lo que hay debajo.")),
        ("building", tr("Flat & foam roofs", "Techos planos y de espuma"), tr("A core test before anything is priced — layer count and deck type decide what's even allowed.", "Una prueba de núcleo antes de cotizar — el número de capas y el tipo de cubierta deciden qué se permite.")),
        ("wrench", tr("Metal roofs", "Techos de metal"), tr("Fasteners first. The share that have failed decides repair versus replacement.", "Primero los tornillos. La proporción que ha fallado decide entre reparar o reemplazar.")),
    ]
    rules = [
        ("doc", tr("Photos before prices", "Primero fotos, después precio"), tr("Every roof is photographed and documented before we put a number on it.", "Cada techo se fotografía y documenta antes de darle un precio.")),
        ("calendar", tr("Priced at the office, in writing", "Cotizado en la oficina, por escrito"), tr("We never guess a number on the roof. You get a written quote you can hold us to.", "Nunca adivinamos un número en el techo. Usted recibe una cotización por escrito.")),
        ("shield", tr("Nobody goes up alone", "Nadie sube solo"), tr("A standing rule on every job: no one from our crew is ever on a roof by themselves.", "Una regla en cada trabajo: nadie de nuestro equipo sube solo a un techo.")),
    ]
    return f'''<section class="section {bg}">
  <div class="container">
    <div class="section-head wide">
      <p class="eyebrow">{tr('How we inspect', 'Cómo inspeccionamos')}</p>
      <h2>{tr('A different checklist for every kind of roof.', 'Una lista de revisión diferente para cada tipo de techo.')}</h2>
      <p>{tr("A flat roof and a tile roof fail for completely different reasons, so one generic sheet doesn't cut it. Whatever is on your house now, we inspect it with a form built for that roof.", "Un techo plano y uno de teja fallan por razones distintas, así que una hoja genérica no sirve. Lo que tenga su casa hoy, lo revisamos con un formato hecho para ese techo.")}</p>
    </div>
    <div class="grid g4">{cards(types)}</div>
    <ul class="points rules reveal">{points(rules)}</ul>
  </div>
</section>
'''


# ---------------------------------------------------------------- pages

def page_home():
    rules = [
        ("doc", tr("Photos before prices", "Primero fotos, después precio"), tr("Every roof is inspected with a checklist for its type and photographed before we put a number on it.", "Cada techo se inspecciona con una lista para su tipo y se fotografía antes de darle un precio.")),
        ("calendar", tr("Quoted in writing", "Cotización por escrito"), tr("Priced at the office, never guessed on the roof — system, color and scope spelled out.", "Se calcula en la oficina, nunca se adivina en el techo — sistema, color y alcance por escrito.")),
        ("shield", tr("Nobody goes up alone", "Nadie sube solo"), tr("A standing rule on every job: no one from our crew is ever on a roof by themselves.", "Una regla en cada trabajo: nadie de nuestro equipo sube solo a un techo.")),
    ]
    faqs = [
        (tr("How long does a metal roof last in El Paso?", "¿Cuánto dura un techo de metal en El Paso?"),
         tr("It depends on the system and how it's installed. A 24-gauge standing seam roof typically lasts 40–70 years. On exposed-fastener roofs like R-panel, the panel lasts decades but the screw washers are a maintenance item — in our sun they can start failing at 10–15 years.",
            "Depende del sistema y de la instalación. Un techo standing seam calibre 24 dura típicamente de 40 a 70 años. En techos con tornillos expuestos como el R-panel, el panel dura décadas pero las arandelas son mantenimiento — con nuestro sol pueden fallar a los 10–15 años.")),
        (tr("Can you replace my shingle roof with metal?", "¿Pueden cambiar mi techo de tejas por metal?"),
         tr(f'Yes. On our El Paso conversion we tore the shingles off to the bare deck, covered the roof in self-sealing membrane and installed 26-gauge R-panel. <a href="{url("shingle")}">How a conversion works</a>.',
            f'Sí. En nuestro cambio en El Paso quitamos las tejas hasta la cubierta, cubrimos todo con membrana autoadherible e instalamos R-panel calibre 26. <a href="{url("shingle")}">Cómo funciona el cambio</a>.')),
        (tr("How much does a metal roof cost?", "¿Cuánto cuesta un techo de metal?"),
         tr("Every roof is different — size, pitch, what's on it now and which system you choose. We inspect, photograph and measure, then give you a clear written quote.",
            "Cada techo es diferente — tamaño, inclinación, lo que tiene ahora y el sistema que elija. Inspeccionamos, fotografiamos y medimos, y le damos una cotización clara por escrito.")),
        ("¿Hablan español?", f"Sí. Se habla español — llámenos al <a href=\"tel:{TEL}\">{PHONE}</a>."),
    ]
    return head(
        tr("Metal Roofing & Siding in El Paso, TX | Manifest Metals", "Techos de Metal en El Paso, TX | Manifest Metals"),
        tr("Standing seam and R-panel metal roofs, shingle-to-metal conversions and metal wall panels for El Paso homes and businesses. Se habla español.",
           "Techos de metal standing seam y R-panel, cambios de tejas a metal y paneles de pared para casas y negocios en El Paso. Se habla español."),
        image="el3", extra_ld=[faq_ld(faqs)],
    ) + header() + f'''
<section class="photo-hero home dark">
  <div class="photo-hero-img">{img("el3", tr("Light Stone R-panel metal roof installed by Manifest Metals on an El Paso home", "Techo R-panel Light Stone instalado por Manifest Metals en una casa de El Paso"), eager=True)}</div>
  <div class="container">
    <p class="eyebrow">{tr('Metal roofing & siding · El Paso, Texas', 'Techos y revestimiento de metal · El Paso, Texas')}</p>
    <h1>{tr('Metal roofs, <em>installed right.</em>', 'Techos de metal, <em>bien instalados.</em>')}</h1>
    <p class="lead">{tr('Standing seam and R-panel roofing, shingle-to-metal conversions and metal wall panels — for homes and businesses across El Paso County, with projects from here to the Gulf Coast.', 'Techos standing seam y R-panel, cambios de tejas a metal y paneles de pared — para casas y negocios en todo el condado de El Paso, con proyectos de aquí hasta la costa del Golfo.')}</p>
    <div class="hero-cta">
      {quote_btn()}
      {tel_btn("btn btn-lg btn-ghost", tr("Call " + PHONE, "Llame al " + PHONE))}
    </div>
    <ul class="hero-tags">
      <li>{icon('chat')}<span lang="es">Se habla español</span></li>
      <li>{icon('pin')}{tr('Locally owned', 'Negocio local')}</li>
      <li>{icon('building')}{tr('Residential & commercial', 'Residencial y comercial')}</li>
    </ul>
    <p class="slide-cap mono"><span class="dot" aria-hidden="true"></span>{tr('El Paso, TX · R-panel · a real Manifest job', 'El Paso, TX · R-panel · un trabajo real de Manifest')}</p>
  </div>
</section>

<section class="section-tight choose">
  <div class="container">
    <h2 class="visually-hidden">{tr('Choose your project', 'Elija su proyecto')}</h2>
    <div class="grid g2">
      <a class="audience reveal" href="{url('residential')}">
        <div class="audience-img">{img("job5", tr("Standing seam roof on a new home", "Techo standing seam en una casa nueva"), "(max-width: 960px) 100vw, 50vw")}</div>
        <p class="eyebrow">{tr('For homeowners', 'Para propietarios')}</p>
        <h3>{tr("A metal roof for your home.", "Un techo de metal para su casa.")}</h3>
        <p>{tr('Standing seam and R-panel roofs, shingle-to-metal conversions, metal siding and carports.', 'Techos standing seam y R-panel, cambios de tejas a metal, revestimiento de metal y cocheras.')}</p>
        <span class="link-arrow">{tr('Residential roofing', 'Techos residenciales')}</span>
      </a>
      <a class="audience reveal" href="{url('commercial')}">
        <div class="audience-img">{img("gv3", tr("Crew tied off on a standing seam roof", "Equipo asegurado en un techo standing seam"), "(max-width: 960px) 100vw, 50vw")}</div>
        <p class="eyebrow">{tr('For GCs, architects & owners', 'Para contratistas, arquitectos y propietarios')}</p>
        <h3>{tr('Put us on your bid list.', 'Inclúyanos en su lista de licitantes.')}</h3>
        <p>{tr("Metal wall panel and roofing scopes for commercial projects. Send plans and specs and we'll get you a number.", "Paneles de pared y techos de metal para proyectos comerciales. Envíe planos y especificaciones y le damos un precio.")}</p>
        <span class="link-arrow">{tr('Commercial', 'Comercial')}</span>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head wide">
      <p class="eyebrow">{tr('Featured project', 'Proyecto destacado')}</p>
      <h2>{tr('A shingle-to-metal conversion, right here in El Paso.', 'Un cambio de tejas a metal, aquí en El Paso.')}</h2>
    </div>
    {project_elpaso(compact=True)}
    <p class="fine-center"><a class="link-arrow" href="{url('projects')}">{tr('More of our work — Galveston and the Houston area', 'Más de nuestro trabajo — Galveston y el área de Houston')}</a></p>
  </div>
</section>

<section class="section bone">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">{tr('Why Manifest', 'Por qué Manifest')}</p>
      <h2>{tr('The careful way, on every roof.', 'Con cuidado, en cada techo.')}</h2>
    </div>
    <ul class="points rules reveal">{points(rules)}</ul>
  </div>
</section>

<section class="section sand">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">{tr('Two systems', 'Dos sistemas')}</p>
      <h2>{tr("Two systems. We'll tell you honestly which one fits.", "Dos sistemas. Le decimos con honestidad cuál le conviene.")}</h2>
    </div>
    {systems()}
  </div>
</section>

{visualizer()}
{process("bone")}
{faq_block(faqs)}
{cta_band()}
''' + footer()


def page_residential():
    what = [
        ("roof", tr("Standing seam roofs", "Techos standing seam"), tr("24 ga, concealed clips and clean lines — built for a long life under desert sun.", "Calibre 24, clips ocultos y líneas limpias — hecho para durar bajo el sol del desierto.")),
        ("home", tr("R-panel roofs", "Techos R-panel"), tr("A strong, economical 26 ga metal roof for homes, casitas and outbuildings.", "Un techo de metal calibre 26 resistente y económico para casas, casitas y bodegas.")),
        ("sun", tr("Shingle-to-metal conversions", "Cambios de tejas a metal"), tr("Tear-off to the deck, new membrane, new metal — a longer-lasting alternative to reroofing with shingles.", "Retiro hasta la cubierta, membrana nueva, metal nuevo — una alternativa más duradera que volver a poner tejas.")),
        ("wall", tr("Metal siding", "Revestimiento de metal"), tr("Metal wall panels for homes, shops and garages — clean lines that hold up to sun and wind.", "Paneles de pared de metal para casas, talleres y garajes — líneas limpias que aguantan el sol y el viento.")),
        ("building", tr("Carports & patio covers", "Cocheras y techos de patio"), tr("Metal roofs for carports, patio covers and outbuildings — the right panel for the slope.", "Techos de metal para cocheras, patios y bodegas — el panel correcto para la pendiente.")),
        ("wrench", tr("Metal roof repairs", "Reparaciones de techos de metal"), tr("Failed fasteners, leaks and flashing — inspected, documented and priced in writing.", "Tornillos fallados, goteras y tapajuntas — inspeccionados, documentados y cotizados por escrito.")),
    ]
    why = [
        ("sun", tr("Built for UV", "Hecho para el sol"), tr("Standing seam has no screws through the panel face. On exposed-fastener roofs, the rubber washers can start failing at 10–15 years in the sun.", "El standing seam no tiene tornillos en la cara del panel. En los techos con tornillos expuestos, las arandelas pueden empezar a fallar a los 10–15 años con el sol.")),
        ("calendar", tr("Built to last", "Hecho para durar"), tr("A 24-gauge standing seam roof typically lasts 40–70 years (industry range, not a warranty).", "Un techo standing seam calibre 24 dura típicamente de 40 a 70 años (rango de la industria, no una garantía).")),
        ("leaf", tr("Cooler on peak days", "Más fresco en los días pico"), tr(f"The {epa('EPA reports')} reflective cool roofs can cut peak cooling demand 11–27% in air-conditioned buildings.", f"La {epa('EPA reporta')} que los techos frescos reflectantes pueden reducir la demanda máxima de enfriamiento entre 11% y 27%.")),
        ("storm", tr("Ready for monsoon and hail", "Listo para el monzón y el granizo"), tr("Interlocking panels shed hard rain, and many metal systems are tested to UL 2218 Class 4 for impact.", "Los paneles entrelazados desalojan la lluvia fuerte, y muchos sistemas de metal están probados bajo UL 2218 Clase 4.")),
    ]
    handy = [
        tr("The property address", "La dirección de la propiedad"),
        tr("Roof, siding, or both", "Techo, revestimiento, o ambos"),
        tr("What's on it now — shingle, tile, foam, metal", "Qué tiene ahora — tejas, teja de barro, espuma, metal"),
        tr("Photos, if you have them", "Fotos, si las tiene"),
        tr("When you'd like the work done", "Cuándo le gustaría hacer el trabajo"),
    ]
    faqs = [
        (tr("Can metal go over my existing roof?", "¿Se puede poner metal sobre mi techo actual?"),
         tr("It depends on what's there now, how many layers there are and the condition of the deck. We inspect first and tell you what your roof actually needs.", "Depende de lo que tiene ahora, cuántas capas hay y la condición de la cubierta. Primero inspeccionamos y le decimos lo que su techo realmente necesita.")),
        (tr("My roof is almost flat. Can it be metal?", "Mi techo es casi plano. ¿Puede ser de metal?"),
         tr("Snap-lock standing seam and R-panel both need at least a 3:12 pitch. Flatter roofs need a different system — we'll look at yours and tell you straight.", "El standing seam snap-lock y el R-panel necesitan al menos una inclinación de 3:12. Los techos más planos necesitan otro sistema — revisamos el suyo y le decimos con claridad.")),
        (tr("Which colors can I choose?", "¿Qué colores puedo elegir?"),
         tr(f'Twelve on our R-panel chart — try them in the <a href="{url("home", anchor="#colors")}">color visualizer</a>. We bring physical chips to your site visit.', f'Doce en nuestra carta de R-panel — pruébelos en el <a href="{url("home", anchor="#colors")}">visualizador de colores</a>. Llevamos muestras físicas a la visita.')),
        (tr("Do you handle the permit?", "¿Ustedes tramitan el permiso?"),
         tr("Yes. When the job needs a permit, we pull it and schedule the inspections.", "Sí. Cuando el trabajo requiere permiso, nosotros lo tramitamos y programamos las inspecciones.")),
        (tr("How much does it cost?", "¿Cuánto cuesta?"),
         tr("It depends on size, pitch, what's on the roof now and which system you choose. We inspect, photograph and measure, then give you a clear written quote.", "Depende del tamaño, la inclinación, lo que tiene el techo ahora y el sistema que elija. Inspeccionamos, fotografiamos y medimos, y le damos una cotización clara por escrito.")),
    ]
    return head(
        tr("Residential Metal Roofing in El Paso | Manifest Metals", "Techos de Metal Residenciales en El Paso | Manifest Metals"),
        tr("Standing seam and R-panel metal roofs, shingle-to-metal conversions, metal siding and carports for El Paso homes. Se habla español.",
           "Techos de metal standing seam y R-panel, cambios de tejas a metal, revestimiento y cocheras para casas en El Paso."),
        image="el3", extra_ld=[faq_ld(faqs)], crumb=tr("Residential", "Residencial"),
    ) + header() + photo_hero(
        "el3", tr("Light Stone R-panel metal roof on an El Paso home", "Techo R-panel Light Stone en una casa de El Paso"),
        tr("Residential", "Residencial"),
        tr("Metal roofs and siding for El Paso homes.", "Techos y revestimiento de metal para casas en El Paso."),
        tr("Standing seam and R-panel roofing, shingle-to-metal conversions and metal siding — inspected, quoted in writing and installed by our crew.", "Techos standing seam y R-panel, cambios de tejas a metal y revestimiento — inspeccionados, cotizados por escrito e instalados por nuestro equipo."),
    ) + f'''
<section class="section">
  <div class="container">
    <div class="section-head"><p class="eyebrow">{tr('What we do', 'Lo que hacemos')}</p><h2>{tr('Roofing and siding, done in metal.', 'Techos y revestimiento, en metal.')}</h2></div>
    <div class="grid g3">{cards(what)}</div>
  </div>
</section>
<section class="section bone">
  <div class="container">
    <div class="section-head wide"><p class="eyebrow">{tr('Real project', 'Proyecto real')}</p><h2>{tr('Shingle to metal, right here in El Paso.', 'De tejas a metal, aquí en El Paso.')}</h2></div>
    {project_elpaso()}
  </div>
</section>
<section class="section">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">{tr('Why homeowners switch', 'Por qué cambian los propietarios')}</p>
      <h2>{tr('Made for West Texas weather.', 'Hecho para el clima del oeste de Texas.')}</h2>
      <ul class="points">{points(why)}</ul>
    </div>
    {lifespan_chart()}
  </div>
</section>
<section class="section sand">
  <div class="container">
    <div class="section-head"><p class="eyebrow">{tr('Pick your system', 'Elija su sistema')}</p><h2>{tr('Standing seam or R-panel?', '¿Standing seam o R-panel?')}</h2></div>
    {systems()}
  </div>
</section>
{inspection()}
{insurance()}
{process("bone")}
<section class="section-tight">
  <div class="container split">
    <div><p class="eyebrow">{tr('Before you call', 'Antes de llamar')}</p><h2>{tr('Have these handy.', 'Tenga esto a la mano.')}</h2><p class="lead">{tr("It helps us give you a straight answer on the first call.", "Nos ayuda a darle una respuesta clara desde la primera llamada.")}</p></div>
    <div class="panel accent reveal"><ul class="checks">{"".join(f"<li>{h}</li>" for h in handy)}</ul>{tel_btn("btn btn-block")}</div>
  </div>
</section>
{faq_block(faqs, "bone")}
{cta_band()}
''' + footer()


def page_shingle():
    steps = [
        (tr("Inspect the shingle roof", "Inspeccionamos el techo de tejas"), tr("Hail test squares on every slope, the vents and soft metals, and a look at the deck and attic ventilation.", "Cuadros de prueba de granizo en cada pendiente, ventilas y metales, y una revisión de la cubierta y la ventilación del ático.")),
        (tr("Tear off to the deck", "Retiramos hasta la cubierta"), tr("On our El Paso conversion the shingles came off down to bare wood, and every bit was hauled away. Any bad decking is replaced — approved by you, in writing.", "En nuestro cambio en El Paso las tejas se quitaron hasta la madera y todo se desechó. La cubierta dañada se reemplaza — con su aprobación por escrito.")),
        (tr("Seal the whole roof", "Sellamos todo el techo"), tr("Self-sealing waterproof membrane over the entire deck before any metal goes on.", "Membrana impermeable autoadherible en toda la cubierta antes de poner el metal.")),
        (tr("Metal and trim", "Metal y remates"), tr("Panels, then color-matched ridge, rake and edge trim, and sidewall and transition flashing.", "Paneles, y luego cumbreras, remates y tapajuntas del mismo color.")),
        (tr("Every penetration", "Cada penetración"), tr("New seals on pipes and vents, turbines and roof jacks — the places a roof usually leaks.", "Sellos nuevos en tubos, ventilas, turbinas y chimeneas — donde normalmente gotea un techo.")),
        (tr("Clean up and walk it", "Limpiamos y lo recorremos"), tr("Daily cleanup, a magnet sweep of the yard and driveway, and a final walk of the roof with you.", "Limpieza diaria, barrido con imán del patio y la entrada, y un recorrido final del techo con usted.")),
    ]
    step_html = "".join(f'<li class="step reveal"><h3>{t}</h3><p>{d}</p></li>' for t, d in steps)
    rows = [
        (tr("Typical life in our sun", "Vida típica con nuestro sol"), tr("Often 15–20 years", "Con frecuencia 15–20 años"), tr("40–70 years (24 ga standing seam)", "40–70 años (standing seam calibre 24)")),
        (tr("Hail", "Granizo"), tr("Granules knocked loose, bruising", "Pierde gránulos, se golpea"), tr("Many systems tested to UL 2218 Class 4 — ask which", "Muchos sistemas probados bajo UL 2218 Clase 4 — pregunte cuáles")),
        (tr("Heat", "Calor"), tr("Dark shingles absorb sun", "Las tejas oscuras absorben el sol"), tr(f"Reflective finishes available; per the {epa('EPA')}, cool roofs can cut peak cooling demand 11–27%", f"Acabados reflectantes; según la {epa('EPA')}, los techos frescos pueden bajar la demanda máxima de enfriamiento 11–27%")),
        (tr("Wind", "Viento"), tr("Tabs lift and crack", "Las pestañas se levantan y agrietan"), tr("Interlocking panels", "Paneles entrelazados")),
    ]
    sh, mt = tr("Asphalt shingles", "Tejas de asfalto"), tr("Metal", "Metal")
    body_rows = "".join(f'<tr><th scope="row">{k}</th><td data-label="{sh}">{a}</td><td data-label="{mt}">{b}</td></tr>' for k, a, b in rows)
    faqs = [
        (tr("Will you put metal over my shingles?", "¿Ponen metal sobre mis tejas?"),
         tr("It depends on the layers and the deck. On our El Paso conversion we removed the shingles down to the deck so we could see the wood, fix what needed fixing and seal the whole roof before the metal went on.", "Depende de las capas y la cubierta. En nuestro cambio en El Paso quitamos las tejas hasta la cubierta para ver la madera, reparar lo necesario y sellar todo el techo antes del metal.")),
        (tr("How long does a conversion take?", "¿Cuánto tarda un cambio?"),
         tr("It depends on the size of the roof and the color you choose — in-stock colors usually start sooner than special orders. We give you a timeline with the written quote.", "Depende del tamaño del techo y del color que elija — los colores en existencia normalmente empiezan antes que los pedidos especiales. Le damos el tiempo estimado con la cotización.")),
        (tr("Does my insurance cover it?", "¿Lo cubre mi seguro?"),
         tr("If your shingles have hail damage, it might. We document the roof the way an adjuster checks it — test squares on every slope — so you have a clear record for your claim.", "Si sus tejas tienen daño por granizo, podría. Documentamos el techo como lo revisa un ajustador — cuadros de prueba en cada pendiente — para que tenga un registro claro.")),
        (tr("Do you pull the permit?", "¿Ustedes tramitan el permiso?"),
         tr("Yes. When the job needs a permit, we pull it and schedule the inspections.", "Sí. Cuando el trabajo requiere permiso, nosotros lo tramitamos y programamos las inspecciones.")),
    ]
    return head(
        tr("Replace Shingles With a Metal Roof in El Paso | Manifest Metals", "Cambie sus Tejas por un Techo de Metal en El Paso | Manifest Metals"),
        tr("Shingle-to-metal roof conversions in El Paso: tear-off to the deck, waterproof membrane and a 26 ga R-panel or 24 ga standing seam roof. See a real El Paso project.",
           "Cambios de tejas a metal en El Paso: retiro hasta la cubierta, membrana impermeable y un techo R-panel calibre 26 o standing seam calibre 24."),
        image="el1", extra_ld=[faq_ld(faqs)], crumb=tr("Shingle to metal", "De tejas a metal"),
    ) + header() + photo_hero(
        "el1", tr("New R-panel metal roof on an El Paso home that used to have shingles", "Techo R-panel nuevo en una casa de El Paso que antes tenía tejas"),
        tr("Shingle to metal", "De tejas a metal"),
        tr("Tired of reroofing? Go metal.", "¿Cansado de retejar? Cámbiese a metal."),
        tr("We replace worn shingle roofs with 26-gauge R-panel or 24-gauge standing seam — torn off to the deck, sealed, and built for El Paso sun.", "Cambiamos techos de tejas gastados por R-panel calibre 26 o standing seam calibre 24 — retirados hasta la cubierta, sellados y hechos para el sol de El Paso."),
    ) + f'''
<section class="section">
  <div class="container">
    <div class="section-head wide"><p class="eyebrow">{tr('Shingles vs metal', 'Tejas vs metal')}</p><h2>{tr('Why El Paso homeowners make the switch.', 'Por qué los propietarios de El Paso hacen el cambio.')}</h2></div>
    <div class="reveal"><table class="compare"><thead><tr><th scope="col"><span class="visually-hidden">{tr('Feature', 'Característica')}</span></th><th scope="col">{sh}</th><th scope="col">{mt}</th></tr></thead><tbody>{body_rows}</tbody></table></div>
    <p class="fine-center">{tr('Typical ranges. Actual life depends on the product, ventilation and installation.', 'Rangos típicos. La vida real depende del producto, la ventilación y la instalación.')}</p>
  </div>
</section>
<section class="section bone">
  <div class="container">
    <div class="section-head"><p class="eyebrow">{tr('What a conversion includes', 'Qué incluye el cambio')}</p><h2>{tr('Six steps, done right.', 'Seis pasos, bien hechos.')}</h2></div>
    <ol class="steps six">{step_html}</ol>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head wide"><p class="eyebrow">{tr('Real project', 'Proyecto real')}</p><h2>{tr('Here is one we finished in El Paso.', 'Este lo terminamos en El Paso.')}</h2></div>
    {project_elpaso()}
  </div>
</section>
{insurance()}
{faq_block(faqs, "bone")}
{cta_band()}
''' + footer()


def page_commercial():
    scope = [
        ("wall", tr("Metal wall panels", "Paneles de pared de metal"), tr("Wall panel scopes for new construction, re-skins and panel replacement — including color matching against existing panels.", "Paneles de pared para obra nueva, remodelaciones y reemplazo de paneles — incluyendo igualar colores con paneles existentes.")),
        ("roof", tr("Standing seam roofing", "Techos standing seam"), tr("24 ga, 1-3/4&quot; snap-lock, concealed clips — for commercial and institutional buildings.", "Calibre 24, snap-lock de 1-3/4&quot;, clips ocultos — para edificios comerciales e institucionales.")),
        ("building", tr("R-panel roofing", "Techos R-panel"), tr("26 ga exposed-fastener panels for warehouses, shops and pre-engineered buildings.", "Paneles calibre 26 con tornillos expuestos para bodegas, talleres y edificios prefabricados.")),
        ("wrench", tr("Repairs & retrofits", "Reparaciones y renovaciones"), tr("Failed fasteners, leaks, flashing and panel replacement on existing metal buildings.", "Tornillos fallados, goteras, tapajuntas y reemplazo de paneles en edificios de metal existentes.")),
    ]
    why = [
        ("doc", tr("Clear, written bids", "Cotizaciones claras por escrito"), tr("Scope, exclusions and schedule spelled out, so there are no surprises at buyout.", "Alcance, exclusiones y calendario por escrito, para que no haya sorpresas.")),
        ("shield", tr("A crew that works safe", "Un equipo que trabaja seguro"), tr("Harnesses and tie-offs on the roof, and nobody ever goes up alone.", "Arneses y líneas de vida en el techo, y nadie sube solo nunca.")),
        ("pin", tr("El Paso based", "Con base en El Paso"), tr("A local crew for El Paso County — with standing seam projects as far as Houston and Galveston.", "Un equipo local para el condado de El Paso — con proyectos de standing seam hasta Houston y Galveston.")),
        ("chat", tr("Bilingual", "Bilingüe"), tr("Se habla español — on the phone and on site.", "Se habla español — por teléfono y en la obra.")),
    ]
    send = [
        tr("Project name and location", "Nombre y ubicación del proyecto"),
        tr("Plans and roof / wall panel specs", "Planos y especificaciones de paneles de techo / pared"),
        tr("Bid due date", "Fecha límite de la cotización"),
        tr("Expected construction schedule", "Calendario de construcción previsto"),
        tr("Your prequalification packet — tell us what paperwork and references you need", "Su paquete de precalificación — díganos qué documentos y referencias necesita"),
    ]
    subject = tr("Bid%20invitation", "Invitaci%C3%B3n%20a%20licitar")
    return head(
        tr("Commercial Metal Roofing & Wall Panels in El Paso | Manifest Metals", "Techos y Paneles de Metal Comerciales en El Paso | Manifest Metals"),
        tr("Metal wall panel and roofing packages for GCs, architects and owners — standing seam, R-panel and wall panels. El Paso based, projects across Texas.",
           "Paquetes de paneles de pared y techos de metal para contratistas, arquitectos y propietarios. Con base en El Paso, proyectos en todo Texas."),
        image="gv3", crumb=tr("Commercial", "Comercial"),
    ) + header() + photo_hero(
        "gv3", tr("Manifest crew tied off on a standing seam roof", "Equipo de Manifest asegurado en un techo standing seam"),
        tr("Commercial", "Comercial"),
        tr("Metal wall panel and roofing packages for commercial projects.", "Paquetes de paneles de pared y techos de metal para proyectos comerciales."),
        tr("We bid metal wall panel, standing seam and R-panel scopes for general contractors, architects and owners — based in El Paso, with projects across Texas.", "Cotizamos paneles de pared, standing seam y R-panel para contratistas generales, arquitectos y propietarios — con base en El Paso y proyectos en todo Texas."),
    ) + f'''
<section class="section">
  <div class="container">
    <div class="section-head"><p class="eyebrow">{tr('Scope', 'Alcance')}</p><h2>{tr('What we bid.', 'Lo que cotizamos.')}</h2></div>
    <div class="grid g4">{cards(scope)}</div>
  </div>
</section>
<section class="section bone">
  <div class="container split top">
    <div class="reveal">
      <p class="eyebrow">{tr('Why sub to us', 'Por qué subcontratarnos')}</p>
      <h2>{tr('A metal subcontractor that answers the phone.', 'Un subcontratista de metal que contesta el teléfono.')}</h2>
      <ul class="points">{points(why)}</ul>
    </div>
    <div class="panel accent reveal" id="bid">
      <p class="eyebrow">{tr('Bidding a project?', '¿Cotizando un proyecto?')}</p>
      <h3>{tr("Send us the package and we'll get you a number.", "Envíenos el paquete y le damos un precio.")}</h3>
      <ul class="checks">{"".join(f"<li>{s}</li>" for s in send)}</ul>
      <a class="btn btn-block" href="mailto:{EMAIL}?subject={subject}">{icon('doc')}{tr('Email plans & specs', 'Enviar planos por correo')}</a>
      <a class="btn btn-block btn-ghost" href="{url('contact')}?type=commercial#quote">{tr('Or use the bid form', 'O use el formulario')}</a>
      <p class="form-fine" style="margin-top:14px">{tr('Or call', 'O llame al')} <a href="tel:{TEL}">{PHONE}</a>.</p>
    </div>
  </div>
</section>
<section class="section sand">
  <div class="container">
    <div class="section-head"><p class="eyebrow">{tr('Systems', 'Sistemas')}</p><h2>{tr('Standing seam and R-panel.', 'Standing seam y R-panel.')}</h2></div>
    {systems(homes=False)}
  </div>
</section>
{cta_band()}
''' + footer()


def page_projects():
    return head(
        tr("Our Work: Metal Roofing Projects | Manifest Metals", "Proyectos de Techos de Metal | Manifest Metals"),
        tr("Real Manifest Metals projects: a shingle-to-metal conversion in El Paso and standing seam roofs in Galveston and the Houston area.",
           "Proyectos reales de Manifest Metals: un cambio de tejas a metal en El Paso y techos standing seam en Galveston y el área de Houston."),
        image="gv1", crumb=tr("Our work", "Proyectos"),
    ) + header() + photo_hero(
        "gv1", tr("Manifest crew installing a standing seam roof on a beachfront home", "Equipo de Manifest instalando un techo standing seam frente al mar"),
        tr("Our work", "Proyectos"),
        tr("Real jobs. Real photos.", "Trabajos reales. Fotos reales."),
        tr("Every photo on this page is a Manifest Metals job — from a shingle-to-metal conversion in El Paso to standing seam on the Gulf Coast.", "Cada foto en esta página es un trabajo de Manifest Metals — desde un cambio de tejas a metal en El Paso hasta standing seam en la costa del Golfo."),
    ) + f'''
<section class="section">
  <div class="container projects">
    {project_elpaso("h2")}
    {project_galveston("h2")}
    {project_houston("h2")}
  </div>
</section>
{cta_band()}
''' + footer()


def page_guide():
    rows = [
        (tr("Fasteners", "Fijación"),
         tr("<strong>Concealed clips</strong> under the seam. No screws through the panel face.", "<strong>Clips ocultos</strong> bajo la costura. Sin tornillos en la cara del panel."),
         tr("<strong>Exposed screws</strong> with rubber washers through the panel face.", "<strong>Tornillos expuestos</strong> con arandelas de hule en la cara del panel.")),
        (tr("Steel & panel", "Acero y panel"),
         tr("24 ga · 1-3/4&quot; snap-lock seam · 18&quot; panels", "Calibre 24 · costura snap-lock de 1-3/4&quot; · paneles de 18&quot;"),
         tr("26 ga · 36&quot; coverage per panel", "Calibre 26 · 36&quot; de cobertura por panel")),
        (tr("In our sun", "Con nuestro sol"),
         tr("No washers in the panel face for UV to break down.", "Sin arandelas en la cara del panel que el sol pueda deteriorar."),
         tr("Washers break down in UV and can start failing at 10–15 years.", "Las arandelas se deterioran con el sol y pueden fallar a los 10–15 años.")),
        (tr("Service life", "Vida útil"),
         tr("40–70 years typical (industry range).", "40–70 años típicos (rango de la industria)."),
         tr("The panel lasts decades; plan on fastener upkeep over time.", "El panel dura décadas; conviene dar mantenimiento a los tornillos con los años.")),
        (tr("Look", "Apariencia"),
         tr("Flat striated pans and tall raised seams. Modern.", "Paneles planos estriados y costuras elevadas. Moderno."),
         tr("Ribbed profile. Classic ranch and industrial look.", "Perfil acanalado. Estilo rancho e industrial.")),
        (tr("Colors", "Colores"),
         tr("A premium color range — ask us.", "Una gama de colores premium — pregúntenos."),
         tr("12 on our chart, including Galvalume.", "12 en nuestra carta, incluyendo Galvalume.")),
        (tr("Minimum pitch", "Inclinación mínima"), "3:12", "3:12"),
        (tr("Upfront cost", "Costo inicial"), tr("Higher.", "Más alto."), tr("Lower.", "Más bajo.")),
    ]
    ss, rp = "Standing seam", "R-panel"
    body_rows = "".join(f'<tr><th scope="row">{k}</th><td data-label="{ss}">{a}</td><td data-label="{rp}">{b}</td></tr>' for k, a, b in rows)
    return head(
        tr("Standing Seam vs R-Panel: Which Metal Roof Is Right? | Manifest Metals", "Standing Seam vs R-Panel: ¿Qué techo de metal le conviene? | Manifest Metals"),
        tr("An honest comparison of standing seam and R-panel metal roofing for El Paso — fasteners, UV, gauge, service life, colors and cost.",
           "Una comparación honesta de techos de metal standing seam y R-panel para El Paso — fijación, sol, calibre, vida útil, colores y costo."),
        image="job2", crumb="Standing seam vs R-panel",
    ) + header() + photo_hero(
        "job2", tr("Standing seam metal roof panels", "Paneles de techo standing seam"),
        tr("Guide", "Guía"),
        tr('Standing seam vs. <span class="nowrap">R-panel</span>: which metal roof is right for you?', 'Standing seam vs. <span class="nowrap">R-panel</span>: ¿qué techo de metal le conviene?'),
        tr("Both are metal. Both last a long time. In El Paso, the real difference is how they're fastened — and what the sun does to those fasteners.", "Los dos son de metal. Los dos duran mucho. En El Paso, la verdadera diferencia es cómo se fijan — y lo que el sol le hace a esa fijación."),
        actions=False,
    ) + f'''
<section class="section">
  <div class="container">
    <div class="section-head"><p class="eyebrow">{tr('The difference, in cross-section', 'La diferencia, en corte')}</p><h2>{tr('Hidden clips vs. exposed screws.', 'Clips ocultos vs. tornillos expuestos.')}</h2></div>
    <div class="grid g2 profiles">
      <figure class="profile reveal"><div class="profile-art">{standing_seam_profile(LANG)}</div><figcaption><strong>Standing seam</strong>{tr('The clip hooks the panel to the deck and hides under the next seam.', 'El clip sujeta el panel a la cubierta y queda oculto bajo la siguiente costura.')}</figcaption></figure>
      <figure class="profile reveal"><div class="profile-art">{r_panel_profile(LANG)}</div><figcaption><strong>R-panel</strong>{tr('Screws with rubber washers go straight through the panel face.', 'Los tornillos con arandelas de hule atraviesan la cara del panel.')}</figcaption></figure>
    </div>
  </div>
</section>
<section class="section bone">
  <div class="container">
    <div class="section-head"><p class="eyebrow">{tr('Side by side', 'Lado a lado')}</p><h2>{tr('How they compare.', 'Cómo se comparan.')}</h2></div>
    <div class="reveal"><table class="compare"><thead><tr><th scope="col"><span class="visually-hidden">{tr('Feature', 'Característica')}</span></th><th scope="col">{ss}</th><th scope="col">{rp}</th></tr></thead><tbody>{body_rows}</tbody></table></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="duo reveal">
      <figure>{img("job4", tr("Standing seam panels on a project roof", "Paneles standing seam en un techo de proyecto"), "(max-width: 960px) 100vw, 50vw")}<figcaption><span class="mono">Standing seam</span>{tr('Flat pans, raised seams, nothing exposed.', 'Paneles planos, costuras elevadas, nada expuesto.')}</figcaption></figure>
      <figure>{img("el3", tr("R-panel roof with exposed fasteners in El Paso", "Techo R-panel con tornillos expuestos en El Paso"), "(max-width: 960px) 100vw, 50vw")}<figcaption><span class="mono">R-panel</span>{tr('Ribbed panels, screws through the face.', 'Paneles acanalados, tornillos en la cara.')}</figcaption></figure>
    </div>
  </div>
</section>
<section class="section bone">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">{tr('Our honest take', 'Nuestra opinión honesta')}</p>
      <h2>{tr("For a home you plan to keep, go standing seam.", "Para una casa que piensa conservar, elija standing seam.")}</h2>
      <p class="lead">{tr("With no screws through the panel face, the part our sun attacks first on a metal roof isn't there — and it looks great. For a shop, barn or a tighter budget, R-panel is a strong, economical roof — just plan on checking fasteners as it ages.", "Sin tornillos en la cara del panel, no está la parte que el sol ataca primero en un techo de metal — y se ve muy bien. Para un taller, un granero o un presupuesto más ajustado, el R-panel es un techo resistente y económico — solo conviene revisar los tornillos con los años.")}</p>
      <p>{tr("Not sure? We'll look at your building and tell you straight.", "¿No está seguro? Revisamos su propiedad y le decimos con claridad.")}</p>
    </div>
    {lifespan_chart()}
  </div>
</section>
{cta_band()}
''' + footer()


def page_about():
    values = [
        ("doc", tr("Photos before prices", "Primero fotos, después precio"), tr("Every roof is photographed and documented before we put a number on it.", "Cada techo se fotografía y documenta antes de darle un precio.")),
        ("calendar", tr("Quotes in writing", "Cotizaciones por escrito"), tr("Priced at the office, never guessed on the roof — system, color and scope spelled out.", "Calculadas en la oficina, nunca adivinadas en el techo — sistema, color y alcance por escrito.")),
        ("shield", tr("Nobody goes up alone", "Nadie sube solo"), tr("No one from our crew is ever on a roof by themselves. Every job, every time.", "Nadie de nuestro equipo sube solo a un techo. En cada trabajo, siempre.")),
        ("chat", tr("Se habla español", "Se habla español"), tr("On the phone, in the quote and on the roof.", "Por teléfono, en la cotización y en el techo.")),
    ]
    return head(
        tr("About Manifest Metals | Metal Roofing in El Paso", "Nosotros | Manifest Metals, techos de metal en El Paso"),
        tr("Manifest Metals, LLC is a locally owned El Paso company installing metal roofing and siding on homes and commercial buildings.",
           "Manifest Metals, LLC es una empresa local de El Paso que instala techos y revestimiento de metal en casas y edificios comerciales."),
        image="gv2", crumb=tr("About", "Nosotros"),
    ) + header() + photo_hero(
        "gv2", tr("Manifest crew installing standing seam panels", "Equipo de Manifest instalando paneles standing seam"),
        tr("About", "Nosotros"),
        tr("A metal roofing company that does it the careful way.", "Una empresa de techos de metal que trabaja con cuidado."),
        tr("Manifest Metals, LLC is locally owned in El Paso and installs metal roofing and siding on homes and commercial buildings — from El Paso County to the Gulf Coast.", "Manifest Metals, LLC es un negocio local de El Paso que instala techos y revestimiento de metal en casas y edificios comerciales — del condado de El Paso a la costa del Golfo."),
    ) + f'''
<section class="section">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">{tr('What we believe', 'Lo que creemos')}</p>
      <h2>{tr('The right roof for this climate is metal.', 'El techo correcto para este clima es de metal.')}</h2>
      <p class="lead">{tr("Close to 300 days of sun a year, a hard monsoon and spring hail. We think metal — and especially standing seam — is the best answer to El Paso weather, and we'd rather show you why than sell you something.", "Casi 300 días de sol al año, un monzón fuerte y granizo en primavera. Creemos que el metal — y sobre todo el standing seam — es la mejor respuesta al clima de El Paso, y preferimos mostrarle por qué antes que venderle algo.")}</p>
      <p>{tr("So we keep it simple: we inspect with a checklist built for your roof, photograph everything, price it at the office, put it in writing and install it right.", "Por eso lo hacemos sencillo: inspeccionamos con una lista hecha para su techo, fotografiamos todo, cotizamos en la oficina, lo ponemos por escrito y lo instalamos bien.")}</p>
    </div>
    <figure class="stack-photo reveal">{img("gv1", tr("Our crew installing a standing seam roof on a beachfront home", "Nuestro equipo instalando un techo standing seam frente al mar"), "(max-width: 960px) 100vw, 50vw")}</figure>
  </div>
</section>
<section class="section bone">
  <div class="container">
    <div class="section-head"><p class="eyebrow">{tr('How we work', 'Cómo trabajamos')}</p><h2>{tr('What you can expect.', 'Lo que puede esperar.')}</h2></div>
    <div class="grid g4">{cards(values)}</div>
  </div>
</section>
{cta_band()}
''' + footer()


def page_contact():
    msgs = {
        "invalid": tr("Please add your name, a phone number and a few project details — and check the email address if you added one.", "Por favor agregue su nombre, un teléfono y algunos detalles del proyecto — y revise el correo si lo agregó."),
        "sending": tr("Sending…", "Enviando…"),
        "ok": tr("Thanks — we got it. We'll call you back soon.", "Gracias — lo recibimos. Le llamaremos pronto."),
        "fail": tr(f"Something went wrong. Please call us at {PHONE}.", f"Algo salió mal. Por favor llámenos al {PHONE}."),
    }
    msg_attrs = "".join(f' data-msg-{k}="{v}"' for k, v in msgs.items())

    def choice(name, val, label, checked=False):
        return f'<label class="choice"><input type="radio" name="{name}" value="{val}"{" checked" if checked else ""}><span>{label}</span></label>'
    color_opts = f'<option value="Not sure">{tr("Not sure yet", "Aún no sé")}</option>' + "".join(
        f'<option value="{en}">{tr(en, es)}</option>' for _, en, es, _ in COLORS)
    areas = "".join(f"<li>{a}</li>" for a in AREAS)
    next_steps = [
        tr("We call you back to talk it through.", "Le devolvemos la llamada para platicarlo."),
        tr("We set a time to inspect, photograph and measure.", "Programamos una visita para inspeccionar, fotografiar y medir."),
        tr("You get a written quote — no guesses on the roof.", "Recibe una cotización por escrito — sin adivinar en el techo."),
    ]
    return head(
        tr("Contact Manifest Metals | Metal Roofing Quote in El Paso", "Contacto | Cotización de techo de metal en El Paso | Manifest Metals"),
        tr(f"Call {PHONE} or request a quote for metal roofing or siding in El Paso. Se habla español.", f"Llame al {PHONE} o pida una cotización para techos o revestimiento de metal en El Paso."),
        image=None, crumb=tr("Contact", "Contacto"),
    ) + header() + f'''
<section class="page-hero dark">
  <div class="container">
    <nav class="crumbs" aria-label="{tr('Breadcrumb', 'Ruta')}"><a href="{url('home')}">{tr('Home', 'Inicio')}</a><span aria-hidden="true">/</span>{tr('Contact', 'Contacto')}</nav>
    <h1>{tr("Let's talk about your roof.", "Hablemos de su techo.")}</h1>
    <p class="lead">{tr("Call to set up a time to inspect and measure, or send us a few details and we'll get back to you.", "Llame para programar una visita, o envíenos algunos datos y nos comunicamos con usted.")}</p>
  </div>
</section>
<section class="section" id="quote">
  <div class="container contact-grid">
    <div class="contact-side">
      <div class="phone-card reveal">
        <p class="eyebrow">{tr('Fastest way to reach us', 'La forma más rápida')}</p>
        <a class="big" href="tel:{TEL}">{PHONE}</a>
        <p>{tr('Call or tap to dial.', 'Llame o toque para marcar.')} <span lang="es">Se habla español.</span></p>
        <ul class="kv">
          <li><span>Email</span><span><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
          <li><span>{tr('Based in', 'Ubicación')}</span><span>{tr('El Paso County, Texas', 'Condado de El Paso, Texas')}</span></li>
          <li><span>{tr('GCs', 'Contratistas')}</span><span>{tr('Email plans, specs and bid date', 'Envíe planos, especificaciones y fecha de licitación')}</span></li>
        </ul>
      </div>
      <div class="next reveal">
        <p class="eyebrow">{tr('What happens next', 'Qué sigue')}</p>
        <ol>{"".join(f"<li>{s}</li>" for s in next_steps)}</ol>
      </div>
      <div class="reveal">
        <p class="eyebrow">{tr('Service area', 'Área de servicio')}</p>
        <ul class="areas">{areas}</ul>
        <p class="form-fine" style="margin-top:12px">{tr('Larger and commercial projects across Texas.', 'Proyectos grandes y comerciales en todo Texas.')}</p>
      </div>
    </div>
    <div class="panel reveal">
      <h2 class="form-title">{tr('Request a quote', 'Pida una cotización')}</h2>
      <p class="form-intro">{tr("Tell us a bit about the project. We'll call you back.", "Cuéntenos un poco sobre el proyecto. Le devolvemos la llamada.")}</p>
      <form class="form" id="quote-form" novalidate data-endpoint="{FORM_ENDPOINT}"{msg_attrs}>
        <input type="hidden" name="_subject" value="{tr('New quote request — Manifest Metals website', 'Nueva solicitud (español) — sitio de Manifest Metals')}">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="page_language" value="{tr('English', 'Español')}">
        <div class="hp" aria-hidden="true"><label>Leave empty<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
        <fieldset class="choices field">
          <legend>{tr('Project type', 'Tipo de proyecto')}</legend>
          {choice("project_type", "Residential", tr("Home", "Casa"), True)}
          {choice("project_type", "Commercial", tr("Commercial / bid", "Comercial / licitación"))}
        </fieldset>
        <div class="commercial-only" hidden>
          <div class="row">
            <div class="field"><label for="f-project">{tr('Project name', 'Nombre del proyecto')}</label><input class="input" id="f-project" name="project_name"></div>
            <div class="field"><label for="f-company">{tr('Company', 'Empresa')}</label><input class="input" id="f-company" name="company" autocomplete="organization"></div>
          </div>
          <div class="row">
            <div class="field"><label for="f-bid">{tr('Bid due date', 'Fecha límite de la cotización')} <span class="opt">({tr('optional', 'opcional')})</span></label><input class="input" id="f-bid" name="bid_due" type="date"></div>
            <div class="field"><label for="f-plans">{tr('Link to plans', 'Enlace a los planos')} <span class="opt">({tr('optional', 'opcional')})</span></label><input class="input" id="f-plans" name="plans_link" type="url" inputmode="url" placeholder="https://"></div>
          </div>
        </div>
        <fieldset class="choices field">
          <legend>{tr('What do you need?', '¿Qué necesita?')}</legend>
          {choice("service", "New / replacement roof", tr("New roof", "Techo nuevo"), True)}
          {choice("service", "Shingle to metal", tr("Shingle to metal", "De tejas a metal"))}
          {choice("service", "Siding / wall panels", tr("Siding / wall panels", "Revestimiento / paredes"))}
          {choice("service", "Repair", tr("Repair", "Reparación"))}
          {choice("service", "Carport / patio", tr("Carport / patio", "Cochera / patio"))}
        </fieldset>
        <div class="row">
          <div class="field"><label for="f-name">{tr('Name', 'Nombre')}</label><input class="input" id="f-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="f-phone">{tr('Phone', 'Teléfono')}</label><input class="input" id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
        </div>
        <div class="row">
          <div class="field"><label for="f-email">Email <span class="opt">({tr('optional', 'opcional')})</span></label><input class="input" id="f-email" name="email" type="email" autocomplete="email"></div>
          <div class="field"><label for="f-area">{tr('Project location', 'Ubicación del proyecto')}</label><input class="input" id="f-area" name="area" autocomplete="address-level2"></div>
        </div>
        <div class="row">
          <div class="field"><label for="f-color">{tr('Color in mind?', '¿Color en mente?')} <span class="opt">({tr('optional', 'opcional')})</span></label><select class="select" id="f-color" name="color">{color_opts}</select></div>
          <div class="field"><label for="f-lang">{tr('Preferred language', 'Idioma preferido')}</label><select class="select" id="f-lang" name="preferred_language"><option>{tr('English', 'Español')}</option><option>{tr('Español', 'English')}</option></select></div>
        </div>
        <div class="field"><label for="f-details">{tr('Project details', 'Detalles del proyecto')}</label><textarea class="textarea" id="f-details" name="details" required placeholder="{tr('What’s on the roof now, rough size, timing, anything else…', 'Qué tiene el techo ahora, tamaño aproximado, cuándo, cualquier otro detalle…')}"></textarea></div>
        <button class="btn btn-lg btn-block" type="submit">{tr('Send request', 'Enviar solicitud')}</button>
        <p class="form-status" role="status" aria-live="polite"></p>
        <p class="form-fine">{tr("We'll only use your info to reply about your project.", "Solo usaremos sus datos para responder sobre su proyecto.")} <a href="{url('privacy')}">{tr('Privacy', 'Privacidad')}</a></p>
      </form>
    </div>
  </div>
</section>
''' + footer(ridge_on="")


def page_privacy():
    sections = [
        (tr("What we collect", "Qué recopilamos"),
         tr("Only what you type into the quote form — your name, phone, email if you add it, project location and project details — or what you tell us when you call or email.",
            "Solo lo que escribe en el formulario — su nombre, teléfono, correo si lo agrega, ubicación y detalles del proyecto — o lo que nos dice al llamar o escribir.")),
        (tr("How the form works", "Cómo funciona el formulario"),
         tr('The quote form is delivered to our email by <a href="https://formsubmit.co/" rel="noopener">FormSubmit</a>, a form-forwarding service. It passes your message along to us; see their site for how they handle data.',
            'El formulario llega a nuestro correo a través de <a href="https://formsubmit.co/" rel="noopener">FormSubmit</a>, un servicio para reenviar formularios. Solo nos pasa su mensaje; consulte su sitio para saber cómo manejan los datos.')),
        (tr("How we use it", "Cómo lo usamos"),
         tr("To reply to you about your project, schedule an inspection and send your quote. We don't sell your information or add you to a mailing list.",
            "Para responderle sobre su proyecto, programar una inspección y enviarle su cotización. No vendemos su información ni lo agregamos a listas de correo.")),
        (tr("Cookies and tracking", "Cookies y rastreo"),
         tr("This site doesn't set advertising cookies. Fonts and images are served from this site. If we add visitor analytics later, we'll update this page.",
            "Este sitio no usa cookies de publicidad. Las fuentes e imágenes se sirven desde este sitio. Si más adelante agregamos analíticas de visitas, actualizaremos esta página.")),
        (tr("Questions or removal", "Preguntas o eliminación"),
         tr(f'Email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{TEL}">{PHONE}</a> and we\'ll delete what you sent us.',
            f'Escriba a <a href="mailto:{EMAIL}">{EMAIL}</a> o llame al <a href="tel:{TEL}">{PHONE}</a> y borraremos lo que nos envió.')),
    ]
    body = "".join(f"<h2>{h}</h2><p>{t}</p>" for h, t in sections)
    return head(
        tr("Privacy | Manifest Metals", "Privacidad | Manifest Metals"),
        tr("How Manifest Metals handles the information you send through our website.", "Cómo maneja Manifest Metals la información que nos envía por el sitio."),
        image=None, crumb=tr("Privacy", "Privacidad"),
    ) + header() + f'''
<section class="page-hero dark">
  <div class="container">
    <nav class="crumbs" aria-label="{tr('Breadcrumb', 'Ruta')}"><a href="{url('home')}">{tr('Home', 'Inicio')}</a><span aria-hidden="true">/</span>{tr('Privacy', 'Privacidad')}</nav>
    <h1>{tr("Privacy", "Privacidad")}</h1>
    <p class="lead">{tr("Short version: we use what you send us to answer you, and nothing else.", "En corto: usamos lo que nos envía para responderle, y nada más.")}</p>
  </div>
</section>
<section class="section"><div class="container prose">{body}</div></section>
''' + footer(ridge_on="")


def page_404():
    return head("Page not found | Manifest Metals", "Page not found.", image=None) + header() + f'''
<section class="section notfound"><div class="container">
  <div class="code">404</div>
  <h1 style="font-size:clamp(1.8rem,3vw,2.6rem)">{tr("This page isn't here.", "Esta página no existe.")}</h1>
  <p class="lead" style="margin:0 auto 28px">{tr("Let's get you back on track.", "Volvamos al inicio.")}</p>
  <div class="hero-cta" style="justify-content:center"><a class="btn btn-lg" href="{url('home')}">{tr('Go home', 'Ir al inicio')}</a>{tel_btn("btn btn-lg btn-ghost")}</div>
</div></section>
''' + footer(ridge_on="")


BUILDERS = {
    "home": page_home, "residential": page_residential, "commercial": page_commercial,
    "projects": page_projects, "shingle": page_shingle, "guide": page_guide,
    "about": page_about, "contact": page_contact, "privacy": page_privacy,
}


def write(path, html):
    full = os.path.join(ROOT, path) if path.endswith(".html") else os.path.join(ROOT, path, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    return full


def main():
    global LANG, CURRENT
    written = []
    for key, builder in BUILDERS.items():
        for lang in ("en", "es"):
            LANG, CURRENT = lang, key
            written.append(write(PAGES[key][lang], builder()))
    # 404 is served at any depth, so it uses root-absolute paths
    LANG, CURRENT = "en", "home"
    html = page_404()
    prefixes = ["assets/"] + sorted({p[lg] for p in PAGES.values() for lg in ("en", "es") if p[lg]}, key=len, reverse=True)
    for prefix in prefixes:
        html = html.replace(f'href="{prefix}', f'href="/{prefix}').replace(f'src="{prefix}', f'src="/{prefix}')
    html = html.replace('href="./"', 'href="/"')
    written.append(write("404.html", html))

    urls = "".join(
        f'<url><loc>{SITE_URL}/{p[lg]}</loc>'
        + "".join(f'<xhtml:link rel="alternate" hreflang="{l2}" href="{SITE_URL}/{p[l2]}"/>' for l2 in ("en", "es"))
        + "</url>"
        for p in PAGES.values() for lg in ("en", "es")
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                f'xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}</urlset>\n')
    print(f"Built {len(written)} pages")


if __name__ == "__main__":
    main()
