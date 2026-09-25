"""Inline SVG illustrations and icons for the Manifest Metals site."""


def standing_seam_profile(lang="en"):
    clip = "Concealed clip" if lang == "en" else "Clip oculto"
    seam = "Raised seam" if lang == "en" else "Costura elevada"
    base = 104
    seams_x = [40, 250, 460]
    d = f"M0,{base}"
    for sx in seams_x:
        d += f" L{sx - 5},{base} L{sx - 5},{base - 56} L{sx - 2},{base - 62} L{sx + 5},{base - 62} L{sx + 5},{base}"
    d += f" L520,{base}"
    striations = "".join(
        f'<line x1="{x}" y1="{base - 1}" x2="{x + 8}" y2="{base - 1}" stroke="#8f959e" stroke-width="1.2" opacity=".7"/>'
        for x in range(60, 520, 22) if all(abs(x - s) > 18 for s in seams_x)
    )
    clips = "".join(
        f'<path d="M{sx - 20},{base + 1} L{sx - 5},{base + 1} L{sx - 5},{base - 30}" fill="none" stroke="#e2733a" stroke-width="4" stroke-linejoin="round"/>'
        for sx in seams_x
    )
    return f'''<svg viewBox="0 0 520 170" role="img" aria-label="{'Standing seam panel cross-section' if lang == 'en' else 'Corte de panel standing seam'}">
  <rect x="0" y="{base + 4}" width="520" height="14" fill="#3a3f47"/>
  <path d="M0,{base + 4} L520,{base + 4}" stroke="#555b64" stroke-width="1"/>
  {"".join(f'<line x1="{x}" y1="{base + 4}" x2="{x - 10}" y2="{base + 18}" stroke="#2b2f36" stroke-width="2"/>' for x in range(14, 530, 14))}
  <path d="{d} L520,{base + 3} L0,{base + 3} Z" fill="#4b515a" opacity=".35"/>
  {clips}
  <path d="{d}" fill="none" stroke="#e9ecef" stroke-width="3.5" stroke-linejoin="round"/>
  {striations}
  <line x1="250" y1="{base - 70}" x2="250" y2="14" stroke="#a7acb3" stroke-width="1" stroke-dasharray="3 3"/>
  <text x="258" y="20" fill="#e9ecef" font-family="Plex Mono, monospace" font-size="13" letter-spacing="1">{seam.upper()}</text>
  <line x1="440" y1="{base - 16}" x2="440" y2="{base + 40}" stroke="#e2733a" stroke-width="1" stroke-dasharray="3 3"/>
  <text x="340" y="{base + 58}" fill="#f3a55c" font-family="Plex Mono, monospace" font-size="13" letter-spacing="1">{clip.upper()}</text>
</svg>'''


def r_panel_profile(lang="en"):
    fast = "Exposed fastener + washer" if lang == "en" else "Tornillo expuesto + arandela"
    rib = "Major rib" if lang == "en" else "Costilla mayor"
    base = 104
    d = f"M0,{base}"
    ribs = [20, 190, 360]
    for rx in ribs:
        d += f" L{rx},{base} L{rx + 14},{base - 40} L{rx + 34},{base - 40} L{rx + 48},{base}"
        for m in (rx + 88, rx + 122):
            d += f" L{m},{base} L{m + 4},{base - 4} L{m + 10},{base - 4} L{m + 14},{base}"
    d += f" L520,{base}"
    screws = ""
    for sx in (100, 270, 440):
        screws += (
            f'<line x1="{sx}" y1="{base - 36}" x2="{sx}" y2="{base + 14}" stroke="#c9ccd1" stroke-width="3"/>'
            f'<rect x="{sx - 9}" y="{base - 44}" width="18" height="9" rx="2" fill="#c9ccd1"/>'
            f'<ellipse cx="{sx}" cy="{base - 2}" rx="12" ry="4" fill="#e2733a"/>'
        )
    return f'''<svg viewBox="0 0 520 170" role="img" aria-label="{'R-panel cross-section' if lang == 'en' else 'Corte de panel R-panel'}">
  <rect x="0" y="{base + 4}" width="520" height="14" fill="#3a3f47"/>
  {"".join(f'<line x1="{x}" y1="{base + 4}" x2="{x - 10}" y2="{base + 18}" stroke="#2b2f36" stroke-width="2"/>' for x in range(14, 530, 14))}
  <path d="{d} L520,{base + 3} L0,{base + 3} Z" fill="#4b515a" opacity=".35"/>
  <path d="{d}" fill="none" stroke="#e9ecef" stroke-width="3.5" stroke-linejoin="round"/>
  {screws}
  <line x1="214" y1="{base - 48}" x2="214" y2="14" stroke="#a7acb3" stroke-width="1" stroke-dasharray="3 3"/>
  <text x="222" y="20" fill="#e9ecef" font-family="Plex Mono, monospace" font-size="13" letter-spacing="1">{rib.upper()}</text>
  <line x1="440" y1="{base + 4}" x2="440" y2="{base + 40}" stroke="#e2733a" stroke-width="1" stroke-dasharray="3 3"/>
  <text x="516" y="{base + 58}" text-anchor="end" fill="#f3a55c" font-family="Plex Mono, monospace" font-size="13" letter-spacing="1">{fast.upper()}</text>
</svg>'''


FOOTER_RIDGE = ('<svg class="footer-ridge {cls}" viewBox="0 0 1440 70" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
                '<path fill="currentColor" d="M0,70 L0,52 L80,44 L150,48 L230,30 L290,38 L350,22 L400,30 L460,12 L520,26 '
                'L580,18 L640,34 L720,24 L790,40 L860,30 L930,44 L1010,36 L1090,48 L1170,40 L1250,50 L1340,44 L1440,52 L1440,70 Z"/></svg>')

LOGO = ('<svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
        '<defs><linearGradient id="lg-m" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8793a"/><stop offset="1" stop-color="#b24e1e"/></linearGradient></defs>'
        '<rect width="48" height="48" rx="9" fill="url(#lg-m)"/>'
        '<path d="M11 36V13l13 14 13-14v23" fill="none" stroke="#fff" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="square"/>'
        '<path d="M11 40h26" stroke="#fff" stroke-opacity=".45" stroke-width="2"/></svg>')

_I = {
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5L16 9.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "ruler": '<path d="M3 16L16 3l5 5L8 21z"/><path d="M7 12l2 2M10 9l2 2M13 6l2 2"/>',
    "truck": '<path d="M2 6h12v10H2zM14 10h4l3 3v3h-7"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
    "home": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "building": '<path d="M3 21V8l9-5 9 5v13"/><path d="M8 21v-6h8v6M8 11h.01M12 11h.01M16 11h.01"/>',
    "wall": '<path d="M4 4h16v16H4z"/><path d="M8 4v16M12 4v16M16 4v16"/>',
    "roof": '<path d="M2 13L12 5l10 8"/><path d="M6 10v9M10 7v12M14 7v12M18 10v9"/>',
    "storm": '<path d="M7 16a5 5 0 1 1 1-9.9A6 6 0 0 1 19 9a4 4 0 0 1-1 7.9"/><path d="M12 13l-2 4h4l-2 4"/>',
    "flame": '<path d="M12 3c1 4 5 5.5 5 10a5 5 0 0 1-10 0c0-2.5 1.5-4 2.5-5 .5 2 1.5 3 2.5 3 0-3-1-5 0-8z"/>',
    "chat": '<path d="M4 5h16v10H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6.5 6.5 0 0 1 3.5 6"/>',
    "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7"/>',
    "wrench": '<path d="M14.5 6.5a4 4 0 0 0 5 5L12 19a2.1 2.1 0 0 1-3-3z"/><path d="M14.5 6.5L17 4l3 3-2.5 2.5"/>',
    "leaf": '<path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19l8-8"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "blueprint": '<path d="M3 5h14a3 3 0 0 1 3 3v11H6a3 3 0 0 1-3-3z"/><path d="M3 16a3 3 0 0 1 3-3h14M9 8v5M13 8v5"/>',
}


def icon(name):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>')
