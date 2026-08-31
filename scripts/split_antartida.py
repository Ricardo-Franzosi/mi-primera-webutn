#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "pages" / "bitacora" / "drake-antartida-y-60-rugientes.html"
OUT = ROOT / "pages" / "bitacora" / "antartida"
INDEX = ROOT / "pages" / "bitacora" / "index.html"

SECTIONS = [
    ("cruce-del-drake", "Cruce del Drake", None, "15–20 de diciembre de 2021", "Del Canal Beagle a los 60° Sur."),
    ("isla-decepcion", "Isla Decepción", [r"21\s+de\s+(?:diciembre|enero)"], "21–24 de diciembre de 2021", "La llegada a las Shetland del Sur y los primeros fondeos antárticos."),
    ("gerlache-bahia-paraiso", "Gerlache y Bahía Paraíso", [r"25\s+de\s+diciembre"], "25–29 de diciembre de 2021", "Hacia el estrecho de Gerlache y Bahía Paraíso."),
    ("islas-melchior-canal-murature", "Islas Melchior y Canal Murature", [r"30\s+de\s+diciembre"], "30 de diciembre de 2021 – 2 de enero de 2022", "Los días en el archipiélago de las Islas Melchior."),
    ("regreso-por-el-drake", "Regreso por el Drake", [r"(?:D[ií]a\s+)?3\s+de\s+enero"], "3–7 de enero de 2022", "La partida de la Antártida y el cruce de regreso."),
]


def shell(title, eyebrow, intro, body, prev_item=None, next_item=None):
    nav = []
    if prev_item:
        nav.append(f'<a href="./{prev_item[0]}.html"><span>← Anterior</span><strong>{prev_item[1]}</strong></a>')
    else:
        nav.append('<a href="./index.html"><span>← Índice</span><strong>Etapa antártica</strong></a>')
    if next_item:
        nav.append(f'<a href="./{next_item[0]}.html"><span>Siguiente →</span><strong>{next_item[1]}</strong></a>')
    else:
        nav.append('<a href="../index.html"><span>Volver →</span><strong>Bitácora completa</strong></a>')
    return f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{title} · Etapa antártica del viaje del Atlantis."><meta name="theme-color" content="#0b3440">
<title>{title} · Francho y el Atlantis</title><link rel="stylesheet" href="../../../css/styles.css"><link rel="stylesheet" href="../../../css/bitacora.css"><link rel="icon" type="image/svg+xml" href="../../../assets/favicon.svg"></head>
<body><a class="skip-link" href="#contenido">Saltar al contenido</a>
<header class="site-header"><div class="shell header-inner"><a class="brand" href="../../../index.html"><span class="brand-mark" aria-hidden="true">A</span><span>Francho y el Atlantis</span></a><nav class="nav" aria-label="Navegación principal"><a href="../../../index.html">Inicio</a><a href="../index.html" aria-current="page">Bitácora</a><a href="../../gallery.html">Galería</a><a href="../../tripulacion.html">Tripulación</a><a href="../../atlantis.html">El Atlantis</a><a href="../../about.html">Sobre mí</a></nav></div></header>
<main class="shell" id="contenido"><section class="page-hero chapter-hero"><p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="lead">{intro}</p></section>
<article class="journal-entry card"><div class="journal-entry-body">{body}</div><footer class="journal-source"><span>Texto original de la bitácora</span><a href="https://velero-atlantis.blogspot.com/2022/01/sir-francis-drake-la-antartida-y-los-60.html" target="_blank" rel="noopener noreferrer">Ver publicación completa en Blogger ↗</a></footer></article>
<nav class="chapter-nav" aria-label="Navegación de la etapa antártica">{''.join(nav)}</nav></main>
<footer class="site-footer"><div class="shell footer-inner"><div><strong>Francho y el Atlantis</strong><p>Bitácora personal de navegación.</p></div><div class="footer-links"><a href="../index.html">Bitácora</a><a href="../../gallery.html">Galería</a></div></div></footer></body></html>'''


def find_boundary(content, patterns, after=0):
    for pat in patterns:
        m = re.search(pat, content[after:], flags=re.I|re.S)
        if m:
            absolute = after + m.start()
            p = content.rfind("<p", after, absolute)
            return p if p >= after else absolute
    raise RuntimeError(f"No se encontró límite antártico: {patterns}")


def main():
    text = SRC.read_text(encoding="utf-8")
    m = re.search(r'<div class="journal-entry-body">(.*?)</div>\s*<footer class="journal-source">', text, flags=re.S)
    if not m:
        raise RuntimeError("No se encontró el cuerpo de la entrada antártica")
    content = m.group(1)

    starts = [0]
    cursor = 0
    for _, _, patterns, _, _ in SECTIONS[1:]:
        pos = find_boundary(content, patterns, cursor)
        starts.append(pos)
        cursor = pos + 1
    starts.append(len(content))

    OUT.mkdir(parents=True, exist_ok=True)
    items = []
    for i, (slug, title, _, dates, intro) in enumerate(SECTIONS):
        chunk = content[starts[i]:starts[i+1]].strip()
        if slug == "islas-melchior-canal-murature":
            photo = '''<figure class="chapter-photo-feature"><a href="../../../assets/images/Canal%20Murature%20Islas%20Melchior.JPG" target="_blank" rel="noopener noreferrer"><img src="../../../assets/images/Canal%20Murature%20Islas%20Melchior.JPG" alt="Tripulación antártica en el Canal Murature, archipiélago de las Islas Melchior" loading="lazy"></a><figcaption><strong>Canal Murature · Islas Melchior</strong><span>La tripulación durante la etapa antártica.</span></figcaption></figure>'''
            chunk = photo + chunk
        prev_item = SECTIONS[i-1] if i > 0 else None
        next_item = SECTIONS[i+1] if i + 1 < len(SECTIONS) else None
        (OUT / f"{slug}.html").write_text(shell(title, f"Etapa antártica · {dates}", intro, chunk, prev_item, next_item), encoding="utf-8")
        items.append((slug, title, dates, intro))

    cards = ''.join(f'''<article class="timeline-card"><p class="timeline-date">{dates}</p><h3>{title}</h3><p>{intro}</p><a href="./{slug}.html">Leer capítulo →</a></article>''' for slug,title,dates,intro in items)
    ant_index = f'''<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><meta name="description" content="Etapa antártica de la expedición del Atlantis."><title>Antártida · Francho y el Atlantis</title><link rel="stylesheet" href="../../../css/styles.css"><link rel="stylesheet" href="../../../css/bitacora.css"><link rel="icon" type="image/svg+xml" href="../../../assets/favicon.svg"></head><body>
<header class="site-header"><div class="shell header-inner"><a class="brand" href="../../../index.html"><span class="brand-mark">A</span><span>Francho y el Atlantis</span></a><nav class="nav"><a href="../../../index.html">Inicio</a><a href="../index.html" aria-current="page">Bitácora</a><a href="../../gallery.html">Galería</a><a href="../../tripulacion.html">Tripulación</a><a href="../../atlantis.html">El Atlantis</a></nav></div></header>
<main class="shell"><section class="page-hero logbook-hero"><p class="eyebrow">Etapa V · Antártida</p><h1>Del Drake a las Islas Melchior</h1><p class="lead">La última entrada del blog original contiene un diario completo del tramo antártico. Aquí se presenta en cinco capítulos para facilitar la lectura, sin reescribir el relato.</p><div class="logbook-meta"><span>15 diciembre 2021 – 7 enero 2022</span><span>5 capítulos</span><span>Texto original</span></div></section><section class="antarctic-feature"><img src="../../../assets/images/Canal%20Murature%20Islas%20Melchior.JPG" alt="Tripulación antártica en Canal Murature"><div><p class="eyebrow">Archipiélago de las Islas Melchior</p><h2>Canal Murature</h2><p>Una de las imágenes incorporadas al archivo del viaje queda ahora vinculada al lugar y al momento narrado en la bitácora.</p></div></section><section class="timeline-grid antarctic-grid">{cards}</section><section class="logbook-note"><p class="eyebrow">Archivo original</p><p>La publicación íntegra sigue disponible como una sola entrada tanto en Blogger como dentro del archivo original de esta web.</p><p><a class="text-link" href="../drake-antartida-y-60-rugientes.html">Leer la entrada completa →</a></p></section></main>
<footer class="site-footer"><div class="shell footer-inner"><div><strong>Francho y el Atlantis</strong><p>Bitácora personal de navegación.</p></div><div class="footer-links"><a href="../index.html">Bitácora</a><a href="../../gallery.html">Galería</a></div></div></footer></body></html>'''
    (OUT / "index.html").write_text(ant_index, encoding="utf-8")

    idx = INDEX.read_text(encoding="utf-8")
    idx = idx.replace('href="./drake-antartida-y-60-rugientes.html">Leer capítulo →</a>', 'href="./antartida/index.html">Explorar etapa antártica →</a>')
    INDEX.write_text(idx, encoding="utf-8")

    css_path = ROOT / "css" / "bitacora.css"
    css = css_path.read_text(encoding="utf-8")
    extra = '''\n.chapter-photo-feature{margin:0 0 2rem;overflow:hidden;border:1px solid var(--line);border-radius:var(--radius);background:var(--paper-2)}.chapter-photo-feature img{width:100%;max-height:620px;object-fit:cover;border-radius:0;box-shadow:none;margin:0}.chapter-photo-feature figcaption{display:grid;gap:.2rem;padding:.9rem 1rem;font-family:Inter,ui-sans-serif,system-ui,sans-serif}.chapter-photo-feature figcaption strong{color:var(--navy)}.chapter-photo-feature figcaption span{color:var(--ink-soft);font-size:.9rem}.antarctic-feature{display:grid;grid-template-columns:1.2fr .8fr;gap:1.5rem;align-items:center;margin-bottom:2.5rem;padding:1rem;border:1px solid var(--line);border-radius:var(--radius);background:rgba(255,255,255,.72)}.antarctic-feature img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:18px}.antarctic-feature>div{padding:1rem}.antarctic-feature p:last-child{margin-top:1rem;color:var(--ink-soft)}.antarctic-grid{margin-bottom:3rem}@media(max-width:760px){.antarctic-feature{grid-template-columns:1fr}}\n'''
    if '.chapter-photo-feature' not in css:
        css += extra
        css_path.write_text(css, encoding="utf-8")

if __name__ == "__main__":
    main()
