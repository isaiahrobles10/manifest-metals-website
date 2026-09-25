"""Manifest Metals emblem, redrawn as SVG from manifest-logo-hires.png (2000x1420 grid)."""

W = 18  # line weight on the 2000px grid


def _mirror(pts, axis=995):
    return [(2 * axis - x, y) for x, y in pts]


def _poly(pts):
    return " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)


FEATHER = (
    # outer blade, base at 0,0, tip at 0,-382
    '<path d="M0,0 C-88,-62 -98,-212 0,-382 C98,-212 88,-62 0,0 Z" fill="currentColor"/>'
    # inner vane (tulip top with notch) + quill
    '<path d="M0,-22 C-50,-64 -62,-160 -42,-196 C-28,-214 -12,-200 -8,-150 L8,-150 C12,-200 28,-214 42,-196 '
    'C62,-160 50,-64 0,-22 Z" fill="var(--logo-bg, #fff)"/>'
    '<path d="M0,-150 V-26" stroke="currentColor" stroke-width="7"/>'
)
FEATHERS = [((983, 400), 0), ((655, 493), -44), ((1335, 493), 44), ((400, 612), -90), ((1590, 612), 90)]


def emblem(cls="", title="Manifest Metals"):
    bg = "var(--logo-bg, #fff)"
    s = []
    # rays (drawn first, the sun covers their inner ends)
    for tri in ([(699, 305), (882, 432), (699, 485)], [(362, 537), (628, 537), (548, 630)]):
        for pts in (tri, _mirror(tri)):
            s.append(f'<polygon points="{_poly(pts)}" fill="{bg}" stroke="currentColor" stroke-width="{W}" stroke-linejoin="miter"/>')
    for (x, y), r in FEATHERS:
        s.append(f'<g transform="translate({x} {y}) rotate({r})">{FEATHER}</g>')
    # sun
    s.append(f'<path d="M546,667 A449,240 0 0 1 1444,667 Z" fill="{bg}" stroke="currentColor" stroke-width="{W}"/>')
    # zigzag crown (outer + inner)
    left = [(752, 742), (777, 722), (732, 690), (772, 662), (724, 630), (777, 596), (724, 522)]
    top = [(843, 548), (893, 516), (940, 548), (995, 499), (1050, 548), (1097, 516), (1147, 548)]
    crown = left + top + list(reversed(_mirror(left)))
    s.append(f'<polyline points="{_poly(crown)}" fill="{bg}" stroke="currentColor" stroke-width="{W}" stroke-linejoin="miter"/>')
    ileft = [(768, 552), (820, 562)]
    s.append(f'<polyline points="{_poly([(785,560),(845,572),(893,540),(940,572),(995,524),(1050,572),(1097,540),(1145,572),(1205,560)])}" fill="none" stroke="currentColor" stroke-width="8"/>')
    # shield
    s.append(f'<polyline points="836,822 836,586 1154,586 1154,822" fill="{bg}" stroke="currentColor" stroke-width="{W}"/>')
    # up arrow
    outer = [(995, 604), (1136, 779), (1046, 779), (1046, 881), (995, 922), (944, 881), (944, 779), (854, 779)]
    inner = [(995, 634), (1100, 764), (1029, 764), (1029, 873), (995, 900), (961, 873), (961, 764), (890, 764)]
    s.append(f'<polygon points="{_poly(outer)}" fill="currentColor"/>')
    s.append(f'<polygon points="{_poly(inner)}" fill="{bg}"/>')
    # M: outer line
    half = [(457, 1199), (419, 1199), (419, 667), (612, 667), (650, 697), (688, 697), (995, 953)]
    m_outer = half + list(reversed(_mirror(half)))[1:]
    s.append(f'<polyline points="{_poly(m_outer)}" fill="none" stroke="currentColor" stroke-width="{W}" stroke-linejoin="miter"/>')
    # M: inner line (legs, feet, lower V)
    ihalf = [(457, 712), (457, 1211), (712, 1211), (651, 1170), (651, 866), (995, 1165)]
    m_inner = ihalf + list(reversed(_mirror(ihalf)))[1:]
    s.append(f'<polyline points="{_poly(m_inner)}" fill="none" stroke="currentColor" stroke-width="{W}" stroke-linejoin="miter"/>')
    # M: second (thin) lines
    top2 = [(556, 706), (684, 706), (995, 966)]
    s.append(f'<polyline points="{_poly(top2 + list(reversed(_mirror(top2)))[1:])}" fill="none" stroke="currentColor" stroke-width="{W}"/>')
    low2 = [(671, 1180), (671, 905), (995, 1190)]
    s.append(f'<polyline points="{_poly(low2 + list(reversed(_mirror(low2)))[1:])}" fill="none" stroke="currentColor" stroke-width="{W}"/>')
    label = f'role="img" aria-label="{title}"' if title else 'aria-hidden="true" focusable="false"'
    return (f'<svg class="{cls}" viewBox="0 0 2000 1240" {label}>'
            f'<g fill="none" stroke-linecap="butt">{"".join(s)}</g></svg>')


if __name__ == "__main__":
    import sys
    print(emblem())
