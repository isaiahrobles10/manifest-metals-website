#!/usr/bin/env python3
"""Builds the Manifest Metals website.

Run from the repo root:  python3 _build/build.py
Every page is generated in English and Spanish into the repo root, which
GitHub Pages serves as-is.

Copy rules: no prices; no license, insurance, bonding, warranty, review or
project claims until verified; Texas service area only; energy claims cite
the EPA peak-cooling figure only. Images are renderings, not project photos,
so they are never captioned as completed jobs.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from art import FOOTER_RIDGE, LOGO, icon, r_panel_profile, standing_seam_profile  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_URL = "https://manifestmetals.com"
PHONE = "(915) 861-6436"
TEL = "+19158616436"
# Free form service: get a key at https://web3forms.com with the inbox that should receive leads.
WEB3FORMS_KEY = ""

PAGES = {
    "home": {"en": "", "es": "es/"},
    "residential": {"en": "residential/", "es": "es/residencial/"},
    "commercial": {"en": "commercial/", "es": "es/comercial/"},
    "guide": {"en": "standing-seam-vs-r-panel/", "es": "es/standing-seam-vs-r-panel/"},
    "about": {"en": "about/", "es": "es/nosotros/"},
    "contact": {"en": "contact/", "es": "es/contacto/"},
}

AREAS = ["El Paso", "Horizon City", "Socorro", "San Elizario", "Clint", "Fabens", "Canutillo", "Vinton", "Anthony, TX"]

# Rendered images in assets/img/r/<name>-<width>.webp
IMAGES = {
    "hero": (800, 1600, 2400), "dusk": (800, 1600, 2400), "commercial": (800, 1600, 2400),
    "detail": (800, 1500), "fastener": (800, 1500), "rpanel": (800, 1600),
}
COLORS = [
    ("charcoal", "Charcoal", "Carbón", "#4a4d52"),
    ("black", "Matte Black", "Negro mate", "#232427"),
    ("bronze", "Dark Bronze", "Bronce oscuro", "#4a3a2e"),
    ("slate", "Burnished Slate", "Pizarra", "#5a5147"),
    ("galvalume", "Galvalume", "Galvalume", "#c3c7cb"),
    ("tan", "Desert Tan", "Arena", "#b8a283"),
    ("white", "Bone White", "Blanco hueso", "#e6e2d8"),
    ("red", "Barn Red", "Rojo granero", "#7c2f25"),
]
for key, *_ in COLORS:
    IMAGES["c-" + key] = (800, 1600)
# Real job photos (drone), assets/img/p/
for n in range(1, 6):
    IMAGES[f"job{n}"] = (800, 1280)


def img_path(name, w):
    return f"img/{'p' if name.startswith('job') else 'r'}/{name}-{w}.webp"

LANG = "en"
CURRENT = "home"


def tr(en, es):
    return en if LANG == "en" else es


def url(key, lang=None):
    """Relative link from the current page to another page."""
    lang = lang or LANG
    depth = PAGES[CURRENT][LANG].count("/")
    rel = "../" * depth + PAGES[key][lang]
    return rel or "./"


def asset(path):
    return "../" * PAGES[CURRENT][LANG].count("/") + "assets/" + path


def img(name, alt, sizes="100vw", cls="", eager=False, width=None):
    widths = IMAGES[name]
    srcset = ", ".join(f"{asset(img_path(name, w))} {w}w" for w in widths)
    mid = widths[1] if len(widths) > 1 else widths[0]
    h = int(mid * (2 / 3)) if name in ("detail", "fastener") else int(mid * 9 / 16)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="{asset(img_path(name, mid))}" srcset="{srcset}" sizes="{sizes}" '
            f'width="{mid}" height="{h}" alt="{alt}" {load}>')


def tel_btn(cls="btn", label=None):
    return f'<a class="{cls}" href="tel:{TEL}">{icon("phone")}{label or PHONE}</a>'


def quote_btn(cls="btn btn-lg"):
    return f'<a class="{cls}" href="{url("contact")}#quote">{tr("Request a quote", "Pida una cotización")}</a>'


# ---------------------------------------------------------------- layout

def head(title, desc, image="hero"):
    here = PAGES[CURRENT]
    canonical = SITE_URL + "/" + here[LANG]
    alt = "".join(
        f'<link rel="alternate" hreflang="{lg}" href="{SITE_URL}/{here[lg]}">' for lg in ("en", "es")
    ) + f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}/{here["en"]}">'
    ld = {
        "@context": "https://schema.org",
        "@type": "RoofingContractor",
        "name": "Manifest Metals, LLC",
        "url": SITE_URL + "/",
        "telephone": "+1-915-861-6436",
        "image": SITE_URL + "/assets/img/og.jpg",
        "address": {"@type": "PostalAddress", "addressLocality": "El Paso", "addressRegion": "TX", "addressCountry": "US"},
        "areaServed": [{"@type": "City", "name": a.replace(", TX", "")} for a in AREAS],
        "knowsLanguage": ["en", "es"],
        "description": desc,
    }
    preload = f'<link rel="preload" as="image" href="{asset(img_path(image, IMAGES[image][1]))}" imagesrcset="{", ".join(asset(img_path(image, w)) + f" {w}w" for w in IMAGES[image])}" imagesizes="100vw">' if image else ""
    return f'''<!DOCTYPE html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{alt}
<meta name="theme-color" content="#111317">
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
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip-link" href="#main">{tr('Skip to content', 'Ir al contenido')}</a>
'''


def header():
    items = [
        ("residential", tr("Residential", "Residencial")),
        ("commercial", tr("Commercial", "Comercial")),
        ("guide", tr("Standing Seam vs R-Panel", "Standing Seam vs R-Panel")),
        ("about", tr("About", "Nosotros")),
        ("contact", tr("Contact", "Contacto")),
    ]
    current = ' aria-current="page"'
    links = "".join(f'<a href="{url(k)}"{current if k == CURRENT else ""}>{label}</a>' for k, label in items)
    other = "es" if LANG == "en" else "en"
    return f'''<div class="topbar"><div class="container">
  <ul><li lang="es">Se habla español</li><li>{tr('Locally owned', 'Negocio local')}</li><li>El Paso, Texas</li></ul>
  <a href="tel:{TEL}">{PHONE}</a>
</div></div>
<header class="site-header">
  <div class="container">
    <a class="brand" href="{url('home')}" aria-label="Manifest Metals — {tr('home', 'inicio')}">
      {LOGO}
      <span class="brand-text"><span class="brand-name">Manifest</span><span class="brand-sub">Metals</span></span>
    </a>
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


def footer(ridge_on="on-copper"):
    def col(title, rows):
        return f'<div><h4>{title}</h4><ul>{"".join(rows)}</ul></div>'

    def li(k, label):
        return f'<li><a href="{url(k)}">{label}</a></li>'
    other = "es" if LANG == "en" else "en"
    return f'''</main>
<footer class="site-footer">
  {FOOTER_RIDGE.format(cls=ridge_on)}
  <div class="container">
    <div class="footer-top">
      <div>
        <a class="brand" href="{url('home')}">{LOGO}<span class="brand-text"><span class="brand-name">Manifest</span><span class="brand-sub">Metals</span></span></a>
        <p class="footer-blurb">{tr("Metal roofing and siding for El Paso homes and commercial buildings. Standing seam, R-panel and metal wall panels.", "Techos y revestimiento de metal para casas y edificios comerciales en El Paso. Standing seam, R-panel y paneles de pared.")}</p>
      </div>
      {col(tr('Services', 'Servicios'), [li('residential', tr('Residential roofing', 'Techos residenciales')), li('commercial', tr('Commercial', 'Comercial')), li('guide', 'Standing seam vs R-panel')])}
      {col(tr('Company', 'Empresa'), [li('about', tr('About us', 'Nosotros')), li('contact', tr('Contact', 'Contacto')), f'<li><a href="{url(CURRENT, other)}">{tr("Español", "English")}</a></li>'])}
      <div>
        <h4>{tr('Call us', 'Llámenos')}</h4>
        <ul>
          <li><a class="footer-phone" href="tel:{TEL}">{PHONE}</a></li>
          <li>El Paso, Texas</li>
          <li lang="es">Se habla español</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span id="year">2026</span> Manifest Metals, LLC</span>
      <span>{tr('Project photos are our work. Other images are illustrative renderings.', 'Las fotos de proyectos son de nuestro trabajo. Las demás imágenes son representaciones ilustrativas.')}</span>
    </div>
  </div>
</footer>
<div class="callbar">
  {tel_btn("btn", tr("Call now", "Llamar"))}
  <a class="btn btn-ghost" href="{url('contact')}#quote">{tr('Get a quote', 'Cotizar')}</a>
</div>
<script src="{asset('js/site.js')}" defer></script>
</body>
</html>
'''


def photo_hero(image, alt, crumb, title, lead, actions=True, tall=False):
    crumbs = f'<div class="crumbs"><a href="{url("home")}">{tr("Home", "Inicio")}</a><span>/</span>{crumb}</div>' if crumb else ""
    btns = f'<div class="hero-cta">{quote_btn()}{tel_btn("btn btn-lg btn-ghost")}</div>' if actions else ""
    return f'''<section class="photo-hero dark{' tall' if tall else ''}">
  <div class="photo-hero-img">{img(image, alt, eager=True)}</div>
  <div class="container">
    {crumbs}
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
    {btns}
  </div>
</section>
'''


def faq(items, bg=""):
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


def process(bg=""):
    steps = [
        (tr("Call or send a request", "Llame o envíe su solicitud"), tr("Tell us about the building and what you have in mind — new roof, replacement or siding.", "Cuéntenos sobre la propiedad y lo que tiene en mente — techo nuevo, reemplazo o revestimiento.")),
        (tr("We measure", "Medimos"), tr("We come out, look at the roof or walls and take measurements.", "Vamos a la propiedad, revisamos el techo o las paredes y tomamos medidas.")),
        (tr("Written quote", "Cotización por escrito"), tr("A clear written quote with the system, color and scope spelled out.", "Una cotización clara por escrito con el sistema, el color y el alcance del trabajo.")),
        (tr("Installed", "Instalación"), tr("Our crew installs your roof or siding and cleans up when the job is done.", "Nuestro equipo instala su techo o revestimiento y limpia al terminar.")),
    ]
    items = "".join(f'<li class="step reveal"><h3>{t}</h3><p>{d}</p></li>' for t, d in steps)
    return f'''<section class="section {bg}">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">{tr('How it works', 'Cómo funciona')}</p>
      <h2>{tr('From first call to final cleanup', 'De la primera llamada a la limpieza final')}</h2>
    </div>
    <ol class="steps">{items}</ol>
  </div>
</section>
'''


def lifespan_chart():
    rows = [
        (tr("Standing seam, 24 ga steel", "Standing seam, acero calibre 24"), tr("40–70 yrs", "40–70 años"), 40, 70, ""),
        (tr("Painted corrugated, 29 ga", "Corrugado pintado, calibre 29"), tr("25–40 yrs", "25–40 años"), 25, 40, "muted"),
        (tr("Exposed-fastener washers", "Arandelas de tornillos expuestos"), tr("start failing 10–15", "fallan a los 10–15"), 10, 15, "warn"),
    ]
    bars = "".join(
        f'''<div class="bar-row"><div class="bar-label"><span>{name}</span><span>{val}</span></div>
        <div class="bar-track"><div class="bar-fill {cls}" style="left:{lo / 70 * 100:.2f}%;width:{(hi - lo) / 70 * 100:.2f}%"></div></div></div>'''
        for name, val, lo, hi, cls in rows
    )
    axis = "".join(f"<span>{n}</span>" for n in range(0, 71, 10))
    return f'''<div class="chart-card reveal">
  <h3>{tr('Typical service life', 'Vida útil típica')}</h3>
  <p class="sub">{tr('Years, by system. In our sun, how a roof is fastened matters as much as the metal.', 'Años, por sistema. Con nuestro sol, cómo se fija el techo importa tanto como el metal.')}</p>
  <div class="bars">{bars}</div>
  <div class="bar-axis">{axis}</div>
  <p class="chart-note">{tr('Typical industry ranges. Actual life depends on the product, finish and installation.', 'Rangos típicos de la industria. La vida real depende del producto, el acabado y la instalación.')}</p>
</div>'''


def systems(links=True):
    ss_link = f'<a class="link-arrow" href="{url("guide")}">Standing seam vs R-panel</a>' if links else ""
    rp_link = f'<a class="link-arrow" href="{url("guide")}">{tr("Compare the two", "Compare los dos")}</a>' if links else ""
    return f'''<div class="systems">
  <article class="system reveal">
    <div class="system-photo">{img("job2", tr("Standing seam metal roof panels and ridge, project photo", "Paneles y cumbrera de un techo standing seam, foto de proyecto"), "(max-width: 960px) 100vw, 600px")}</div>
    <div class="system-body">
      <span class="tag">{tr('Our recommendation for homes', 'Nuestra recomendación para casas')}</span>
      <h3>Standing seam</h3>
      <ul class="checks">
        <li>{tr('Concealed clips — no exposed screws for the sun to attack', 'Clips ocultos — sin tornillos expuestos que el sol pueda dañar')}</li>
        <li>{tr('Clean, modern lines with tall raised seams', 'Líneas limpias y modernas con costuras elevadas')}</li>
        <li>{tr('24 ga steel: 40–70 year typical service life', 'Acero calibre 24: vida útil típica de 40 a 70 años')}</li>
      </ul>
      {ss_link}
    </div>
  </article>
  <article class="system reveal">
    <div class="system-photo">{img("fastener", tr("Close-up rendering of R-panel metal roof with exposed screws and washers", "Representación de cerca de un techo R-panel con tornillos y arandelas expuestos"), "(max-width: 960px) 100vw, 600px")}</div>
    <div class="system-body">
      <span class="tag neutral">{tr('Strong & economical', 'Resistente y económico')}</span>
      <h3>R-panel</h3>
      <ul class="checks">
        <li>{tr('Ribbed exposed-fastener panel — strong and economical', 'Panel acanalado con tornillos expuestos — resistente y económico')}</li>
        <li>{tr('A great fit for shops, barns, outbuildings and commercial', 'Ideal para talleres, graneros, bodegas y obras comerciales')}</li>
        <li>{tr('Plan on checking fasteners as the roof ages', 'Conviene revisar los tornillos con los años')}</li>
      </ul>
      {rp_link}
    </div>
  </article>
</div>'''


def visualizer():
    swatches = "".join(
        f'''<button type="button" class="swatch{' active' if i == 0 else ''}" aria-pressed="{'true' if i == 0 else 'false'}" data-src="{asset(f'img/r/c-{key}-1600.webp')}" data-srcset="{asset(f'img/r/c-{key}-800.webp')} 800w, {asset(f'img/r/c-{key}-1600.webp')} 1600w" data-name="{tr(en, es)}"><span class="chip" style="--c:{hexc}"></span><span class="swatch-name">{tr(en, es)}</span></button>'''
        for i, (key, en, es, hexc) in enumerate(COLORS)
    )
    first = COLORS[0][0]
    return f'''<section class="section visualizer-section">
  <div class="container">
    <div class="viz-head">
      <div class="section-head">
        <p class="eyebrow">{tr('Color visualizer', 'Visualizador de colores')}</p>
        <h2>{tr('See your roof in color.', 'Vea su techo a color.')}</h2>
        <p>{tr('Tap a color to see it on a standing seam roof. Lighter colors reflect more of our sun.', 'Toque un color para verlo en un techo standing seam. Los colores claros reflejan más el sol.')}</p>
      </div>
    </div>
    <div class="viz reveal">
      <div class="viz-stage" aria-live="polite">
        {img("c-" + first, tr("Rendering of a home with a standing seam roof in the selected color", "Representación de una casa con techo standing seam en el color seleccionado"), "(max-width: 1240px) 100vw, 1180px", cls="viz-img")}
        <span class="viz-label"><span class="chip" style="--c:{COLORS[0][3]}"></span><span class="viz-name">{tr(COLORS[0][1], COLORS[0][2])}</span></span>
      </div>
      <div class="swatches" role="group" aria-label="{tr('Roof colors', 'Colores de techo')}">{swatches}</div>
      <p class="viz-note">{tr('Rendering. Colors are representative — ask us for the current color chart before you choose.', 'Representación. Los colores son aproximados — pídanos la carta de colores actual antes de elegir.')}</p>
    </div>
  </div>
</section>
'''


def gallery():
    shots = [
        ("job3", tr("Standing seam", "Standing seam"), tr("Dark bronze standing seam metal roof on a large home, drone photo", "Techo standing seam bronce oscuro en una casa grande, foto con dron")),
        ("job2", tr("Ridge & seams", "Cumbrera y costuras"), tr("Close-up of a standing seam ridge and panels", "Detalle de la cumbrera y paneles standing seam")),
        ("job4", tr("Hips & valleys", "Limatesas y limahoyas"), tr("Standing seam roof with hips and valleys during installation", "Techo standing seam con limatesas y limahoyas durante la instalación")),
        ("job5", tr("Complex roofline", "Techo complejo"), tr("Multi-plane standing seam roof on a new home", "Techo standing seam de varios planos en una casa nueva")),
        ("job1", tr("From above", "Desde arriba"), tr("Overhead drone view of a standing seam roof", "Vista aérea con dron de un techo standing seam")),
    ]
    tiles = "".join(
        f'<button type="button" class="g-tile{" g-big" if i == 0 else ""}" data-full="{asset(img_path(n, 1280))}" aria-label="{tr("View photo", "Ver foto")}: {cap}">'
        f'{img(n, alt, "(max-width: 960px) 100vw, 50vw" if i == 0 else "(max-width: 960px) 50vw, 25vw")}<span class="g-cap mono">{cap}</span></button>'
        for i, (n, cap, alt) in enumerate(shots)
    )
    return f'''<section class="section">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">{tr('Our work', 'Nuestro trabajo')}</p>
      <h2>{tr('Standing seam, installed.', 'Standing seam, instalado.')}</h2>
      <p>{tr('Real photos from our standing seam work in the Houston–Galveston area — every hip, valley and ridge finished by our crew.', 'Fotos reales de nuestros trabajos standing seam en el área de Houston–Galveston — cada limatesa, limahoya y cumbrera terminada por nuestro equipo.')}</p>
    </div>
    <div class="gallery reveal">{tiles}</div>
  </div>
  <dialog class="lightbox" aria-label="{tr('Photo', 'Foto')}"><button type="button" class="lb-close" aria-label="{tr('Close', 'Cerrar')}">×</button><img alt=""></dialog>
</section>
'''


def insurance():
    return f'''<section class="section-tight">
  <div class="container">
    <div class="insure reveal">
      <div class="insure-law"><span class="mono">Tex. Ins. Code</span><strong>§2253.002</strong></div>
      <div>
        <p class="eyebrow">{tr('Hail & insurance', 'Granizo y seguro')}</p>
        <h2>{tr('A Class 4 roof can lower your insurance.', 'Un techo Clase 4 puede bajar su seguro.')}</h2>
        <p>{tr("Texas law requires home insurers to offer a premium discount for roofs rated UL 2218 Class 4 for impact resistance. Many metal roof systems carry that rating. Each insurer sets its own discount, and after installation the contractor completes TDI form PC068 for your policy.", "La ley de Texas exige que las aseguradoras ofrezcan un descuento en la prima para techos con clasificación UL 2218 Clase 4 de resistencia al impacto. Muchos sistemas de techo de metal tienen esa clasificación. Cada aseguradora fija su descuento, y después de la instalación el contratista llena el formulario PC068 del TDI para su póliza.")}</p>
        <p class="insure-ask">{tr('Ask us which systems qualify — then ask your insurer what they credit.', 'Pregúntenos qué sistemas califican — y luego pregunte a su aseguradora cuánto descuentan.')}</p>
      </div>
    </div>
  </div>
</section>
'''


# ---------------------------------------------------------------- pages

def page_home():
    facts = [
        ("~300", tr("sunny days a year in El Paso — the sun is what ages a roof here", "días de sol al año en El Paso — el sol es lo que envejece un techo aquí")),
        ("40–70", tr("years of typical service life for 24 ga standing seam", "años de vida útil típica del standing seam calibre 24")),
        ("0", tr("exposed screws on a standing seam roof", "tornillos expuestos en un techo standing seam")),
        ("ES<small>/EN</small>", tr("Se habla español — call and ask for Spanish", "Se habla español — llame y le atendemos en español")),
    ]
    facts_html = "".join(f'<div class="fact"><span class="fact-big">{b}</span><p>{t}</p></div>' for b, t in facts)

    sun_points = [
        ("sun", tr("Screws are the weak point", "Los tornillos son el punto débil"), tr("On exposed-fastener roofs, rubber washers break down in the sun and start failing at 10–15 years.", "En los techos con tornillos expuestos, las arandelas de hule se deterioran con el sol y empiezan a fallar a los 10–15 años.")),
        ("shield", tr("Standing seam hides them", "El standing seam los esconde"), tr("Concealed clips sit under the seam — nothing exposed in the panel face for UV to break down.", "Los clips ocultos quedan bajo la costura — nada expuesto en la cara del panel que el sol pueda deteriorar.")),
        ("leaf", tr("Cooler on the hottest days", "Más fresco en los días más calurosos"), tr("According to the EPA, reflective cool roofs can cut peak cooling demand 11–27% in air-conditioned homes.", "Según la EPA, los techos frescos reflectantes pueden reducir la demanda máxima de enfriamiento entre 11% y 27% en casas con aire acondicionado.")),
        ("storm", tr("Ready for monsoon and hail", "Listo para el monzón y el granizo"), tr("Hail season runs spring through the July–September monsoon. Interlocking metal panels shed hard rain and stand up to wind.", "La temporada de granizo va de la primavera al monzón de julio a septiembre. Los paneles de metal entrelazados desalojan la lluvia y resisten el viento.")),
    ]
    points = "".join(f'<li><span class="ic">{icon(i)}</span><div><strong>{t}</strong><p>{d}</p></div></li>' for i, t, d in sun_points)

    faqs = [
        (tr("How long does a metal roof last in El Paso?", "¿Cuánto dura un techo de metal en El Paso?"),
         tr("It depends on the system. A 24-gauge standing seam roof typically lasts 40–70 years; painted 29-gauge corrugated, 25–40. In our sun, how the panels are fastened matters as much as the metal — exposed-fastener washers start failing at 10–15 years.",
            "Depende del sistema. Un techo standing seam calibre 24 dura típicamente de 40 a 70 años; la lámina corrugada pintada calibre 29, de 25 a 40. Con nuestro sol, cómo se fijan los paneles importa tanto como el metal — las arandelas de los tornillos expuestos empiezan a fallar a los 10–15 años.")),
        (tr("Can a metal roof lower my home insurance?", "¿Un techo de metal puede bajar mi seguro?"),
         tr("It can. Texas requires home insurers to offer a discount for roofs rated UL 2218 Class 4 for impact resistance, and many metal roof systems carry that rating. Each insurer sets its own amount — ask us which systems qualify, then ask your insurer.",
            "Puede. Texas exige que las aseguradoras ofrezcan un descuento para techos con clasificación UL 2218 Clase 4, y muchos sistemas de metal la tienen. Cada aseguradora fija su monto — pregúntenos qué sistemas califican y luego consulte a su aseguradora.")),
        (tr("Standing seam or R-panel — which should I get?", "¿Standing seam o R-panel — cuál me conviene?"),
         tr("For most homes we recommend standing seam: concealed clips, no exposed screws for UV to attack. R-panel is a strong, economical choice for shops, barns and many commercial buildings. We'll walk through both with you.",
            "Para la mayoría de las casas recomendamos standing seam: clips ocultos, sin tornillos expuestos al sol. El R-panel es una opción resistente y económica para talleres, graneros y muchos edificios comerciales. Le explicamos ambos.")),
        (tr("Is a metal roof loud when it rains?", "¿Hace mucho ruido un techo de metal cuando llueve?"),
         tr("Installed over a solid roof deck with underlayment, a metal roof is typically no louder than any other roof.",
            "Instalado sobre una cubierta sólida con membrana, un techo de metal normalmente no hace más ruido que cualquier otro techo.")),
        (tr("How much does a metal roof cost?", "¿Cuánto cuesta un techo de metal?"),
         tr("Every roof is different — size, pitch, what's on it now and which system you choose. We measure and give you a clear written quote.",
            "Cada techo es diferente — tamaño, inclinación, lo que tiene ahora y el sistema que elija. Medimos y le damos una cotización clara por escrito.")),
        ("¿Hablan español?", f"Sí. Se habla español — llámenos al <a href=\"tel:{TEL}\">{PHONE}</a>."),
    ]

    return head(
        tr("Metal Roofing & Siding in El Paso, TX | Manifest Metals", "Techos de Metal en El Paso, TX | Manifest Metals"),
        tr("Standing seam and R-panel metal roofing and metal siding for El Paso homes and commercial buildings. Built for the sun. Se habla español.",
           "Techos de metal standing seam y R-panel y revestimiento de metal para casas y edificios comerciales en El Paso. Hechos para el sol."),
        image="job3",
    ) + header() + f'''
<section class="photo-hero home dark">
  <div class="photo-hero-img kenburns hero-real">{img("job3", tr("Dark bronze standing seam metal roof under a blue sky with clouds", "Techo standing seam bronce oscuro bajo un cielo azul con nubes"), eager=True)}</div>
  <div class="container">
    <p class="eyebrow">{tr('Metal roofing & siding · El Paso, Texas', 'Techos y revestimiento de metal · El Paso, Texas')}</p>
    <h1>{tr('Metal roofs built for <em>El Paso sun.</em>', 'Techos de metal hechos para <em>el sol de El Paso.</em>')}</h1>
    <p class="lead">{tr('Standing seam and R-panel roofing and metal siding for homes and commercial buildings — built to take the UV, the heat and the monsoon.', 'Techos standing seam y R-panel y revestimiento de metal para casas y edificios comerciales — hechos para aguantar el sol, el calor y el monzón.')}</p>
    <div class="hero-cta">
      {quote_btn()}
      {tel_btn("btn btn-lg btn-ghost", tr("Call " + PHONE, "Llame al " + PHONE))}
    </div>
    <ul class="hero-tags">
      <li>{icon('chat')}<span lang="es">Se habla español</span></li>
      <li>{icon('pin')}{tr('Locally owned', 'Negocio local')}</li>
      <li>{icon('building')}{tr('Residential & commercial', 'Residencial y comercial')}</li>
    </ul>
  </div>
</section>

<div class="facts"><div class="container"><div class="facts-inner reveal">{facts_html}</div></div></div>

<section class="section">
  <div class="container">
    <div class="section-head wide">
      <p class="eyebrow">{tr('Built for the desert', 'Hecho para el desierto')}</p>
      <h2>{tr('In El Paso, the enemy is the sun — not the rain.', 'En El Paso, el enemigo es el sol — no la lluvia.')}</h2>
      <p>{tr('We get under 10 inches of rain a year and close to 300 days of sun. What wears a roof out here is UV, day after day — and the first thing it attacks is exposed fasteners.', 'Aquí llueven menos de 10 pulgadas al año y hay casi 300 días de sol. Lo que desgasta un techo es el sol, día tras día — y lo primero que ataca son los tornillos expuestos.')}</p>
    </div>
    <div class="duo reveal">
      <figure>{img("fastener", tr("Rendering of exposed screws and washers on an R-panel roof", "Representación de tornillos y arandelas expuestos en un techo R-panel"), "(max-width: 960px) 100vw, 50vw")}<figcaption><span class="mono">{tr('Exposed fasteners', 'Tornillos expuestos')}</span>{tr('Every screw is a washer the sun is working on.', 'Cada tornillo es una arandela que el sol va deteriorando.')}</figcaption></figure>
      <figure>{img("detail", tr("Rendering of standing seam roof panels with concealed clips", "Representación de paneles standing seam con clips ocultos"), "(max-width: 960px) 100vw, 50vw")}<figcaption><span class="mono">{tr('Concealed clips', 'Clips ocultos')}</span>{tr('Standing seam keeps them under the seam, out of the sun.', 'El standing seam los mantiene bajo la costura, fuera del sol.')}</figcaption></figure>
    </div>
    <div class="split top sun-split">
      <ul class="points reveal">{points}</ul>
      {lifespan_chart()}
    </div>
  </div>
</section>

{gallery()}

{visualizer()}

<section class="section sand">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">{tr('Two systems', 'Dos sistemas')}</p>
      <h2>{tr("Two systems. We'll tell you honestly which one fits.", "Dos sistemas. Le decimos con honestidad cuál le conviene.")}</h2>
    </div>
    {systems()}
  </div>
</section>

{insurance()}

<section class="section">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">{tr('Who we work for', 'Para quién trabajamos')}</p>
      <h2>{tr('Homeowners and builders.', 'Propietarios y constructores.')}</h2>
    </div>
    <div class="grid g2">
      <a class="audience reveal" href="{url('residential')}">
        <div class="audience-img">{img("job5", tr("Standing seam metal roof on a new home", "Techo standing seam en una casa nueva"), "(max-width: 960px) 100vw, 50vw")}</div>
        <p class="eyebrow">{tr('For homeowners', 'Para propietarios')}</p>
        <h3>{tr("A roof you won't think about for decades.", "Un techo en el que no tendrá que pensar por décadas.")}</h3>
        <p>{tr('Standing seam and R-panel roofs and metal siding for El Paso homes, from the first measurement to final cleanup.', 'Techos standing seam y R-panel y revestimiento de metal para casas en El Paso, desde la primera medida hasta la limpieza final.')}</p>
        <span class="link-arrow">{tr('Residential roofing', 'Techos residenciales')}</span>
      </a>
      <a class="audience reveal" href="{url('commercial')}">
        <div class="audience-img">{img("commercial", tr("Rendering of a commercial building with metal wall panels and a standing seam roof", "Representación de un edificio comercial con paneles de pared de metal y techo standing seam"), "(max-width: 960px) 100vw, 50vw")}</div>
        <p class="eyebrow">{tr('For GCs & architects', 'Para contratistas y arquitectos')}</p>
        <h3>{tr('Put us on your bid list.', 'Inclúyanos en su lista de licitantes.')}</h3>
        <p>{tr("Metal roof and wall panel packages for commercial projects. Send plans and specs and we'll get you a number.", "Paquetes de paneles de metal para techos y paredes en proyectos comerciales. Envíe planos y especificaciones y le damos un precio.")}</p>
        <span class="link-arrow">{tr('Commercial', 'Comercial')}</span>
      </a>
    </div>
  </div>
</section>

{process("bone")}
{faq(faqs)}
{cta_band()}
''' + footer()


def page_residential():
    what = [
        ("roof", tr("Standing seam roofs", "Techos standing seam"), tr("Concealed clips and clean lines — the longest-lasting answer to desert sun.", "Clips ocultos y líneas limpias — la opción que más dura bajo el sol del desierto.")),
        ("home", tr("R-panel roofs", "Techos R-panel"), tr("A strong, economical metal roof for homes, shops, casitas and outbuildings.", "Un techo de metal resistente y económico para casas, talleres, casitas y bodegas.")),
        ("wall", tr("Metal siding", "Revestimiento de metal"), tr("Metal wall panels for homes, shops and garages — clean lines that hold up to sun and wind.", "Paneles de pared de metal para casas, talleres y garajes — líneas limpias que aguantan el sol y el viento.")),
    ]
    cards = "".join(f'<div class="card reveal"><div class="ic">{icon(i)}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in what)
    why = [
        ("sun", tr("Built for UV", "Hecho para el sol"), tr("Standing seam has no exposed screws — the washers on exposed-fastener roofs start failing at 10–15 years in the sun.", "El standing seam no tiene tornillos expuestos — las arandelas de los techos con tornillos expuestos empiezan a fallar a los 10–15 años con el sol.")),
        ("calendar", tr("Built to last", "Hecho para durar"), tr("A 24-gauge standing seam roof typically lasts 40–70 years.", "Un techo standing seam calibre 24 dura típicamente de 40 a 70 años.")),
        ("leaf", tr("Cooler on peak days", "Más fresco en los días pico"), tr("The EPA reports reflective cool roofs can cut peak cooling demand 11–27% in air-conditioned homes.", "La EPA reporta que los techos frescos reflectantes pueden reducir la demanda máxima de enfriamiento entre 11% y 27%.")),
        ("flame", tr("Non-combustible", "No combustible"), tr("Metal won't burn — a layer of protection against embers and sparks.", "El metal no se quema — una capa de protección contra brasas y chispas.")),
    ]
    whys = "".join(f'<li><span class="ic">{icon(i)}</span><div><strong>{t}</strong><p>{d}</p></div></li>' for i, t, d in why)
    handy = [
        tr("The property address", "La dirección de la propiedad"),
        tr("Roof, siding, or both", "Techo, revestimiento, o ambos"),
        tr("What's on it now — shingle, tile, foam, metal", "Qué tiene ahora — tejas, teja de barro, espuma, metal"),
        tr("Photos, if you have them", "Fotos, si las tiene"),
        tr("When you'd like the work done", "Cuándo le gustaría hacer el trabajo"),
    ]
    faqs = [
        (tr("Can metal go over my existing roof?", "¿Se puede poner metal sobre mi techo actual?"),
         tr("Sometimes. It depends on what's there now, its condition and what the job requires. We'll tell you after we look at it.", "A veces. Depende de lo que tiene ahora, su condición y lo que requiere el trabajo. Se lo decimos después de revisarlo.")),
        (tr("Which colors can I choose?", "¿Qué colores puedo elegir?"),
         tr("Try the color visualizer on our home page, then ask us for the current color chart when we come out to measure — lighter colors reflect more sun.", "Pruebe el visualizador de colores en nuestra página principal, y pídanos la carta de colores actual cuando vayamos a medir — los colores claros reflejan más el sol.")),
        (tr("Can a metal roof lower my insurance?", "¿Un techo de metal puede bajar mi seguro?"),
         tr("Texas requires home insurers to offer a discount for UL 2218 Class 4 impact-resistant roofs. Ask us which systems carry that rating.", "Texas exige que las aseguradoras ofrezcan un descuento para techos UL 2218 Clase 4. Pregúntenos qué sistemas tienen esa clasificación.")),
        (tr("How much does it cost?", "¿Cuánto cuesta?"),
         tr("It depends on size, pitch, what's on the roof now and which system you choose. We measure and give you a clear written quote.", "Depende del tamaño, la inclinación, lo que tiene el techo ahora y el sistema que elija. Medimos y le damos una cotización clara por escrito.")),
    ]
    return head(
        tr("Residential Metal Roofing in El Paso | Manifest Metals", "Techos de Metal Residenciales en El Paso | Manifest Metals"),
        tr("Standing seam and R-panel metal roofs and metal siding for El Paso homes. Built for the sun. Se habla español.",
           "Techos de metal standing seam y R-panel y revestimiento de metal para casas en El Paso. Hechos para el sol."),
        image="dusk",
    ) + header() + photo_hero(
        "dusk", tr("Rendering of a home with a standing seam metal roof at dusk", "Representación de una casa con techo standing seam al anochecer"),
        tr("Residential", "Residencial"),
        tr("Metal roofs and siding for El Paso homes.", "Techos y revestimiento de metal para casas en El Paso."),
        tr("Standing seam and R-panel roofing and metal siding — measured, quoted in writing and installed by our crew.", "Techos standing seam y R-panel y revestimiento de metal — medidos, cotizados por escrito e instalados por nuestro equipo."),
    ) + f'''
<section class="section">
  <div class="container">
    <div class="section-head"><p class="eyebrow">{tr('What we install', 'Lo que instalamos')}</p><h2>{tr('Roofing and siding, done in metal.', 'Techos y revestimiento, en metal.')}</h2></div>
    <div class="grid g3">{cards}</div>
  </div>
</section>
<section class="section bone">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">{tr('Why homeowners switch', 'Por qué cambian los propietarios')}</p>
      <h2>{tr('Made for West Texas weather.', 'Hecho para el clima del oeste de Texas.')}</h2>
      <ul class="points">{whys}</ul>
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
<section class="section-tight">
  <div class="container">
    <figure class="wide-photo reveal">{img("rpanel", tr("Rendering of a home with a Galvalume R-panel metal roof", "Representación de una casa con techo R-panel Galvalume"), "(max-width: 1240px) 100vw, 1180px")}<figcaption><span class="mono">R-panel · Galvalume</span>{tr('A classic, economical look — shown here on the same home.', 'Un estilo clásico y económico — en la misma casa.')}</figcaption></figure>
  </div>
</section>
{gallery()}
{insurance()}
{process("bone")}
<section class="section-tight">
  <div class="container split">
    <div><p class="eyebrow">{tr('Before you call', 'Antes de llamar')}</p><h2>{tr('Have these handy.', 'Tenga esto a la mano.')}</h2><p class="lead">{tr("It helps us give you a straight answer on the first call.", "Nos ayuda a darle una respuesta clara desde la primera llamada.")}</p></div>
    <div class="panel accent reveal"><ul class="checks">{"".join(f"<li>{h}</li>" for h in handy)}</ul>{tel_btn("btn btn-block")}</div>
  </div>
</section>
{faq(faqs, "bone")}
{cta_band()}
''' + footer()


def page_commercial():
    scope = [
        ("roof", tr("Standing seam roofing", "Techos standing seam"), tr("Concealed-clip metal roofing for commercial and institutional buildings.", "Techos de metal con clips ocultos para edificios comerciales e institucionales.")),
        ("building", tr("R-panel roofing", "Techos R-panel"), tr("Exposed-fastener roof panels for warehouses, shops and pre-engineered buildings.", "Paneles de techo con tornillos expuestos para bodegas, talleres y edificios prefabricados.")),
        ("wall", tr("Metal wall panels", "Paneles de pared de metal"), tr("Metal wall panel scopes for new construction and re-skins.", "Paneles de pared de metal para obra nueva y remodelaciones.")),
    ]
    cards = "".join(f'<div class="card reveal"><div class="ic">{icon(i)}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in scope)
    why = [
        ("roof", tr("Metal is our focus", "El metal es nuestro enfoque"), tr("Roof and wall panels are what we do — not a line item on a shingle crew's list.", "Los paneles de techo y pared son lo que hacemos — no un servicio más de una cuadrilla de tejas.")),
        ("doc", tr("Clear bids", "Cotizaciones claras"), tr("Scope, exclusions and schedule spelled out, so there are no surprises at buyout.", "Alcance, exclusiones y calendario por escrito, para que no haya sorpresas.")),
        ("pin", tr("El Paso based", "Con base en El Paso"), tr("A local crew for projects in El Paso and nearby Texas communities.", "Un equipo local para proyectos en El Paso y comunidades cercanas de Texas.")),
        ("chat", tr("Bilingual", "Bilingüe"), tr("Se habla español — on the phone and on site.", "Se habla español — por teléfono y en la obra.")),
    ]
    whys = "".join(f'<li><span class="ic">{icon(i)}</span><div><strong>{t}</strong><p>{d}</p></div></li>' for i, t, d in why)
    send = [
        tr("Project name and location", "Nombre y ubicación del proyecto"),
        tr("Plans and roof / wall panel specs", "Planos y especificaciones de paneles de techo / pared"),
        tr("Bid due date", "Fecha límite de la cotización"),
        tr("Expected construction schedule", "Calendario de construcción previsto"),
    ]
    return head(
        tr("Commercial Metal Roofing & Wall Panels in El Paso | Manifest Metals", "Techos y Paneles de Metal Comerciales en El Paso | Manifest Metals"),
        tr("Metal roof and wall panel packages for GCs, architects and owners in the El Paso area. Standing seam, R-panel and wall panels.",
           "Paquetes de paneles de metal para techos y paredes para contratistas, arquitectos y propietarios en El Paso."),
        image="commercial",
    ) + header() + photo_hero(
        "commercial", tr("Rendering of a commercial building with metal wall panels", "Representación de un edificio comercial con paneles de pared de metal"),
        tr("Commercial", "Comercial"),
        tr("Metal roof and wall panel packages for commercial projects.", "Paquetes de paneles de metal para techos y paredes en proyectos comerciales."),
        tr("We bid metal roofing and wall panel scopes for general contractors, architects and owners in the El Paso area.", "Cotizamos alcances de techos y paneles de pared de metal para contratistas generales, arquitectos y propietarios en el área de El Paso."),
    ) + f'''
<section class="section">
  <div class="container">
    <div class="section-head"><p class="eyebrow">{tr('Scope', 'Alcance')}</p><h2>{tr('What we bid.', 'Lo que cotizamos.')}</h2></div>
    <div class="grid g3">{cards}</div>
  </div>
</section>
<section class="section bone">
  <div class="container split top">
    <div class="reveal">
      <p class="eyebrow">{tr('Why sub to us', 'Por qué subcontratarnos')}</p>
      <h2>{tr('A metal subcontractor that answers the phone.', 'Un subcontratista de metal que contesta el teléfono.')}</h2>
      <ul class="points">{whys}</ul>
    </div>
    <div class="panel accent reveal" id="bid">
      <p class="eyebrow">{tr('Bidding a project?', '¿Cotizando un proyecto?')}</p>
      <h3>{tr("Send us the package and we'll get you a number.", "Envíenos el paquete y le damos un precio.")}</h3>
      <ul class="checks">{"".join(f"<li>{s}</li>" for s in send)}</ul>
      {tel_btn("btn btn-block")}
      <p class="form-fine" style="margin-top:14px">{tr('Or send the details through our', 'O envíe los datos con nuestro')} <a href="{url('contact')}#quote">{tr('quote form', 'formulario')}</a>.</p>
    </div>
  </div>
</section>
<section class="section sand">
  <div class="container">
    <div class="section-head"><p class="eyebrow">{tr('Systems', 'Sistemas')}</p><h2>{tr('Standing seam and R-panel.', 'Standing seam y R-panel.')}</h2></div>
    {systems()}
  </div>
</section>
{cta_band()}
''' + footer()


def page_guide():
    rows = [
        (tr("Fasteners", "Fijación"),
         tr("<strong>Concealed clips</strong> under the seam. No screws through the panel face.", "<strong>Clips ocultos</strong> bajo la costura. Sin tornillos en la cara del panel."),
         tr("<strong>Exposed screws</strong> with rubber washers through the panel face.", "<strong>Tornillos expuestos</strong> con arandelas de hule en la cara del panel.")),
        (tr("In our sun", "Con nuestro sol"),
         tr("Nothing exposed for UV to break down.", "Nada expuesto que el sol pueda deteriorar."),
         tr("Washers break down in UV and start failing at 10–15 years.", "Las arandelas se deterioran con el sol y empiezan a fallar a los 10–15 años.")),
        (tr("Service life", "Vida útil"),
         tr("24 ga steel: 40–70 years typical.", "Acero calibre 24: 40–70 años típicos."),
         tr("The panel lasts decades; plan on fastener upkeep over time.", "El panel dura décadas; conviene dar mantenimiento a los tornillos con los años.")),
        (tr("Look", "Apariencia"),
         tr("Clean flat pans and tall raised seams. Modern.", "Paneles planos y costuras elevadas. Moderno."),
         tr("Ribbed profile. Classic ranch and industrial look.", "Perfil acanalado. Estilo rancho e industrial.")),
        (tr("Best for", "Ideal para"),
         tr("Homes you plan to keep; premium commercial.", "Casas que piensa conservar; comercial de alta gama."),
         tr("Shops, barns, outbuildings, warehouses, budget-minded projects.", "Talleres, graneros, bodegas, almacenes y proyectos con presupuesto ajustado.")),
        (tr("Upfront cost", "Costo inicial"), tr("Higher.", "Más alto."), tr("Lower.", "Más bajo.")),
    ]
    ss, rp = "Standing seam", "R-panel"
    body_rows = "".join(f'<tr><th scope="row">{k}</th><td data-label="{ss}">{a}</td><td data-label="{rp}">{b}</td></tr>' for k, a, b in rows)
    return head(
        tr("Standing Seam vs R-Panel: Which Metal Roof Is Right? | Manifest Metals", "Standing Seam vs R-Panel: ¿Qué techo de metal le conviene? | Manifest Metals"),
        tr("An honest comparison of standing seam and R-panel metal roofing for El Paso — fasteners, UV, service life, look and cost.",
           "Una comparación honesta de techos de metal standing seam y R-panel para El Paso — fijación, sol, vida útil, apariencia y costo."),
        image="detail",
    ) + header() + photo_hero(
        "detail", tr("Close-up rendering of standing seam metal roof panels", "Representación de cerca de paneles standing seam"),
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
      <figure>{img("fastener", tr("Rendering of R-panel with exposed screws", "Representación de R-panel con tornillos expuestos"), "(max-width: 960px) 100vw, 50vw")}<figcaption><span class="mono">R-panel</span>{tr('Ribbed panels, screws through the face.', 'Paneles acanalados, tornillos en la cara.')}</figcaption></figure>
    </div>
  </div>
</section>
<section class="section bone">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">{tr('Our honest take', 'Nuestra opinión honesta')}</p>
      <h2>{tr("For a home you plan to keep, go standing seam.", "Para una casa que piensa conservar, elija standing seam.")}</h2>
      <p class="lead">{tr("With no exposed fasteners, there's nothing for the sun to break down, and it looks great doing it. For a shop, barn or a tighter budget, R-panel is a strong, economical roof — just plan on checking fasteners as it ages.", "Sin tornillos expuestos, no hay nada que el sol pueda deteriorar, y se ve muy bien. Para un taller, un granero o un presupuesto más ajustado, el R-panel es un techo resistente y económico — solo conviene revisar los tornillos con los años.")}</p>
      <p>{tr("Not sure? We'll look at your building and tell you straight.", "¿No está seguro? Revisamos su propiedad y le decimos con claridad.")}</p>
    </div>
    {lifespan_chart()}
  </div>
</section>
{cta_band()}
''' + footer()


def page_about():
    values = [
        ("roof", tr("Metal is the specialty", "El metal es la especialidad"), tr("Standing seam, R-panel and metal wall panels — roofs and siding in metal.", "Standing seam, R-panel y paneles de pared — techos y revestimiento en metal.")),
        ("chat", tr("Straight answers", "Respuestas claras"), tr("We'll tell you honestly which system fits your building and your budget.", "Le decimos con honestidad qué sistema le conviene a su propiedad y a su presupuesto.")),
        ("doc", tr("Quotes in writing", "Cotizaciones por escrito"), tr("System, color and scope spelled out before any work starts.", "Sistema, color y alcance por escrito antes de empezar.")),
        ("pin", tr("El Paso local", "De El Paso"), tr("Locally owned. We live and work here. Se habla español.", "Negocio local. Vivimos y trabajamos aquí. Se habla español.")),
    ]
    cards = "".join(f'<div class="card reveal"><div class="ic">{icon(i)}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in values)
    return head(
        tr("About Manifest Metals | Metal Roofing in El Paso", "Nosotros | Manifest Metals, techos de metal en El Paso"),
        tr("Manifest Metals is a locally owned El Paso company installing metal roofing and siding on homes and commercial buildings.",
           "Manifest Metals es una empresa local de El Paso que instala techos y revestimiento de metal en casas y edificios comerciales."),
        image="c-charcoal",
    ) + header() + photo_hero(
        "c-charcoal", tr("Rendering of a home with a charcoal standing seam roof", "Representación de una casa con techo standing seam color carbón"),
        tr("About", "Nosotros"),
        tr("El Paso's metal roofing company.", "La empresa de techos de metal de El Paso."),
        tr("Manifest Metals is locally owned and installs metal roofing and siding on homes and commercial buildings across El Paso.", "Manifest Metals es un negocio local que instala techos y revestimiento de metal en casas y edificios comerciales en El Paso."),
    ) + f'''
<section class="section">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">{tr('What we believe', 'Lo que creemos')}</p>
      <h2>{tr('The right roof for this climate is metal.', 'El techo correcto para este clima es de metal.')}</h2>
      <p class="lead">{tr("Close to 300 days of sun a year, a hard monsoon and spring hail. We think metal — and especially standing seam — is the best answer to El Paso weather, and we'd rather tell you why than sell you something.", "Casi 300 días de sol al año, un monzón fuerte y granizo en primavera. Creemos que el metal — y sobre todo el standing seam — es la mejor respuesta al clima de El Paso, y preferimos explicarle por qué antes que venderle algo.")}</p>
      <p>{tr("So we keep it simple: we measure, we explain the options in plain language, we put the quote in writing and we install it right.", "Por eso lo hacemos sencillo: medimos, le explicamos las opciones con claridad, le damos la cotización por escrito y lo instalamos bien.")}</p>
    </div>
    <figure class="stack-photo reveal">{img("job5", tr("Standing seam metal roof on a new home, project photo", "Techo standing seam en una casa nueva, foto de proyecto"), "(max-width: 960px) 100vw, 50vw")}</figure>
  </div>
</section>
<section class="section bone">
  <div class="container">
    <div class="section-head"><p class="eyebrow">{tr('How we work', 'Cómo trabajamos')}</p><h2>{tr('What you can expect.', 'Lo que puede esperar.')}</h2></div>
    <div class="grid g4">{cards}</div>
  </div>
</section>
{cta_band()}
''' + footer()


def page_contact():
    key_attr = f' data-key="{WEB3FORMS_KEY}"' if WEB3FORMS_KEY else ""
    msgs = {
        "invalid": tr("Please add your name, a phone number, and a few project details.", "Por favor agregue su nombre, un teléfono y algunos detalles del proyecto."),
        "sending": tr("Sending…", "Enviando…"),
        "ok": tr("Thanks — we got it. We'll be in touch soon.", "Gracias — lo recibimos. Nos comunicaremos pronto."),
        "fail": tr(f"Something went wrong. Please call us at {PHONE}.", f"Algo salió mal. Por favor llámenos al {PHONE}."),
        "offline": tr(f"Online requests aren't switched on yet — please call us at {PHONE}.", f"Las solicitudes en línea aún no están activas — por favor llámenos al {PHONE}."),
    }
    msg_attrs = "".join(f' data-msg-{k}="{v}"' for k, v in msgs.items())

    def choice(name, val, label, checked=False):
        return f'<label class="choice"><input type="radio" name="{name}" value="{val}"{" checked" if checked else ""}><span>{label}</span></label>'
    colors = "".join(choice("color", en, tr(en, es)) for _, en, es, _ in COLORS[:6]) + choice("color", "Not sure", tr("Not sure", "No sé"), True)
    areas = "".join(f"<li>{a}</li>" for a in AREAS)
    return head(
        tr("Contact Manifest Metals | Metal Roofing Quote in El Paso", "Contacto | Cotización de techo de metal en El Paso | Manifest Metals"),
        tr(f"Call {PHONE} or request a quote for metal roofing or siding in El Paso. Se habla español.", f"Llame al {PHONE} o pida una cotización para techos o revestimiento de metal en El Paso."),
        image=None,
    ) + header() + f'''
<section class="page-hero dark">
  <div class="container">
    <div class="crumbs"><a href="{url('home')}">{tr('Home', 'Inicio')}</a><span>/</span>{tr('Contact', 'Contacto')}</div>
    <h1>{tr("Let's talk about your roof.", "Hablemos de su techo.")}</h1>
    <p class="lead">{tr("Call to set up a time to measure, or send us a few details and we'll get back to you.", "Llame para programar una visita, o envíenos algunos datos y nos comunicamos con usted.")}</p>
  </div>
</section>
<section class="section" id="quote">
  <div class="container contact-grid">
    <div>
      <div class="phone-card reveal">
        <p class="eyebrow">{tr('Fastest way to reach us', 'La forma más rápida')}</p>
        <a class="big" href="tel:{TEL}">{PHONE}</a>
        <p>{tr('Call or tap to dial.', 'Llame o toque para marcar.')} <span lang="es">Se habla español.</span></p>
        <ul class="kv">
          <li><span>{tr('Based in', 'Ubicación')}</span><span>El Paso, Texas</span></li>
          <li><span>{tr('We do', 'Hacemos')}</span><span>{tr('Metal roofing & siding — residential and commercial', 'Techos y revestimiento de metal — residencial y comercial')}</span></li>
          <li><span>{tr('GCs', 'Contratistas')}</span><span>{tr('Send plans, specs and bid date', 'Envíe planos, especificaciones y fecha de licitación')}</span></li>
        </ul>
      </div>
      <div style="margin-top:32px" class="reveal">
        <p class="eyebrow">{tr('Service area', 'Área de servicio')}</p>
        <ul class="areas">{areas}</ul>
      </div>
    </div>
    <div class="panel reveal">
      <h2 style="font-size:clamp(1.7rem,2.6vw,2.2rem)">{tr('Request a quote', 'Pida una cotización')}</h2>
      <p style="color:var(--text-soft);margin-bottom:26px">{tr("Tell us a bit about the project. We'll call you back.", "Cuéntenos un poco sobre el proyecto. Le devolvemos la llamada.")}</p>
      <form class="form" id="quote-form" novalidate{key_attr}{msg_attrs}>
        <input type="hidden" name="subject" value="{tr('New quote request — manifestmetals.com', 'Nueva solicitud de cotización (ES) — manifestmetals.com')}">
        <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off">
        <fieldset class="choices field">
          <legend>{tr('Project type', 'Tipo de proyecto')}</legend>
          {choice("project_type", "Residential", tr("Home", "Casa"), True)}
          {choice("project_type", "Commercial", tr("Commercial / bid", "Comercial / licitación"))}
        </fieldset>
        <fieldset class="choices field">
          <legend>{tr('What do you need?', '¿Qué necesita?')}</legend>
          {choice("service", "New / replacement roof", tr("Roof", "Techo"), True)}
          {choice("service", "Siding", tr("Siding", "Revestimiento"))}
          {choice("service", "Roof + siding", tr("Both", "Ambos"))}
          {choice("service", "Not sure", tr("Not sure", "No sé"))}
        </fieldset>
        <fieldset class="choices field">
          <legend>{tr('Color in mind?', '¿Tiene un color en mente?')} <span class="opt">({tr('optional', 'opcional')})</span></legend>
          {colors}
        </fieldset>
        <div class="row">
          <div class="field"><label for="f-name">{tr('Name', 'Nombre')}</label><input class="input" id="f-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="f-phone">{tr('Phone', 'Teléfono')}</label><input class="input" id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
        </div>
        <div class="row">
          <div class="field"><label for="f-email">Email <span class="opt">({tr('optional', 'opcional')})</span></label><input class="input" id="f-email" name="email" type="email" autocomplete="email"></div>
          <div class="field"><label for="f-area">{tr('Neighborhood or city', 'Colonia o ciudad')}</label><input class="input" id="f-area" name="area" autocomplete="address-level2"></div>
        </div>
        <div class="field"><label for="f-details">{tr('Project details', 'Detalles del proyecto')}</label><textarea class="textarea" id="f-details" name="details" required placeholder="{tr('Roof size, what’s on it now, timing, anything else…', 'Tamaño del techo, qué tiene ahora, cuándo, cualquier otro detalle…')}"></textarea></div>
        <button class="btn btn-lg btn-block" type="submit">{tr('Send request', 'Enviar solicitud')}</button>
        <p class="form-status" role="status" aria-live="polite"></p>
        <p class="form-fine">{tr("We'll only use your info to reply about your project.", "Solo usaremos sus datos para responder sobre su proyecto.")}</p>
      </form>
    </div>
  </div>
</section>
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
    "guide": page_guide, "about": page_about, "contact": page_contact,
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
    for prefix in ("assets/", "residential/", "commercial/", "standing-seam-vs-r-panel/", "about/", "contact/", "es/"):
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
