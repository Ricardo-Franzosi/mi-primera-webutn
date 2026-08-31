#!/usr/bin/env python3
import json, re, html
from pathlib import Path
from urllib.request import urlopen, Request

BLOG_ID = "5210347577865483851"
FEED = f"https://www.blogger.com/feeds/{BLOG_ID}/posts/default?alt=json&max-results=100"
ROOT = Path(__file__).resolve().parents[1]

SLUGS = [
    "introduccion","la-previa","la-despedida","la-meteorologia",
    "salida-a-mar-del-plata","la-tripulacion","de-mdq-a-los-bramadores",
    "los-pagos-a-eolo","un-dia-explosivo","caleta-hornos","golfo-san-jorge",
    "altas-latitudes-navegando-los-80","san-julian-club-nautico-el-delfin",
    "50-rugientes-y-dionisio","ushuaia","drake-antartida-y-60-rugientes"
]
GROUPS = [
    ("Preparativos", range(0,4)),
    ("Rumbo al Sur", range(4,8)),
    ("Patagonia Austral", range(8,14)),
    ("Fin del Mundo", range(14,15)),
    ("Antártida", range(15,16)),
]

def alternate(entry):
    for link in entry.get("link", []):
        if link.get("rel") == "alternate":
            return link.get("href", "#")
    return "#"

def clean_content(raw):
    """Limpia sólo marcado heredado; conserva las palabras del relato."""
    raw = raw.replace("Hernán Sacheri", "Hernán Casciari").replace("Hernan Sacheri", "Hernán Casciari")
    raw = re.sub(r"<script\b[^>]*>.*?</script>", "", raw, flags=re.I|re.S)
    raw = re.sub(r"\s(?:style|class|id)=(['\"]).*?\1", "", raw, flags=re.I|re.S)

    # Word/Blogger suele envolver cada frase en etiquetas sin valor semántico.
    raw = re.sub(r"</?(?:span|font|o:p)\b[^>]*>", "", raw, flags=re.I)

    # Usar la variante de mayor resolución que sirve Blogger y retirar tamaños fijos.
    def clean_img(match):
        tag = match.group(0)
        tag = re.sub(r"\s(?:width|height|border)=(['\"]).*?\1", "", tag, flags=re.I)
        def upgrade_src(src_match):
            quote, url = src_match.group(1), src_match.group(2)
            if "blogger.googleusercontent.com" in url:
                url = re.sub(r"=s\d+(?:-[^?&#\"']+)?$", "=s1600", url)
                url = re.sub(r"=w\d+-h\d+[^?&#\"']*$", "=s1600", url)
            return f"src={quote}{url}{quote}"
        return re.sub(r"src=(['\"])(.*?)\1", upgrade_src, tag, flags=re.I|re.S)
    raw = re.sub(r"<img\b[^>]*>", clean_img, raw, flags=re.I|re.S)

    # Eliminar párrafos puramente vacíos y reducir saltos acumulados del editor antiguo.
    raw = re.sub(r"<p>\s*(?:(?:&nbsp;)|(?:<br\s*/?>)|\s)*</p>", "", raw, flags=re.I)
    raw = re.sub(r"(?:<br\s*/?>\s*){3,}", "<br><br>", raw, flags=re.I)
    return raw.strip()

def esc(s): return html.escape(s or "", quote=True)

def nav(prefix="", current=""):
    links = [
        ("Inicio", f"{prefix}index.html", "inicio"),
        ("Bitácora", f"{prefix}pages/bitacora/index.html", "bitacora"),
        ("Galería", f"{prefix}pages/gallery.html", "galeria"),
        ("Tripulación", f"{prefix}pages/tripulacion.html", "tripulacion"),
        ("El Atlantis", f"{prefix}pages/atlantis.html", "atlantis"),
        ("Sobre mí", f"{prefix}pages/about.html", "about"),
    ]
    out = ['<nav class="nav" aria-label="Navegación principal">']
    for label, href, key in links:
        cur = ' aria-current="page"' if key == current else ""
        out.append(f'<a href="{href}"{cur}>{label}</a>')
    out.append("</nav>")
    return "".join(out)

def page_shell(title, desc, body, current="bitacora", depth=2):
    prefix = "../../" if depth == 2 else "../"
    nav_html = nav(prefix, current)
    return f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#0b3440">
<title>{esc(title)} · Francho y el Atlantis</title>
<link rel="stylesheet" href="{prefix}css/styles.css"><link rel="stylesheet" href="{prefix}css/bitacora.css">
<link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg"></head>
<body><a class="skip-link" href="#contenido">Saltar al contenido</a>
<header class="site-header"><div class="shell header-inner"><a class="brand" href="{prefix}index.html"><span class="brand-mark" aria-hidden="true">A</span><span>Francho y el Atlantis</span></a>{nav_html}</div></header>
{body}
<footer class="site-footer"><div class="shell footer-inner"><div><strong>Francho y el Atlantis</strong><p>Bitácora personal de navegación.</p></div><div class="footer-links"><a href="{prefix}pages/bitacora/index.html">Bitácora</a><a href="{prefix}pages/gallery.html">Galería</a></div></div></footer>
</body></html>'''

def post_page(post, idx, posts):
    prev = posts[idx-1] if idx else None
    nxt = posts[idx+1] if idx+1 < len(posts) else None
    n = []
    if prev:
        n.append(f'<a href="./{prev["slug"]}.html"><span>← Anterior</span><strong>{esc(prev["title"])}</strong></a>')
    if nxt:
        n.append(f'<a href="./{nxt["slug"]}.html"><span>Siguiente →</span><strong>{esc(nxt["title"])}</strong></a>')
    body = f'''<main class="shell" id="contenido">
<section class="page-hero chapter-hero"><p class="eyebrow">Bitácora original · {post["date"]}</p><h1>{esc(post["title"])}</h1>
<p class="lead">Relato escrito durante la travesía y conservado en su redacción original.</p></section>
<article class="journal-entry card"><div class="journal-entry-body">{post["content"]}</div>
<footer class="journal-source"><span>Fuente original</span><a href="{esc(post["url"])}" target="_blank" rel="noopener noreferrer">Ver esta entrada en Blogger ↗</a></footer></article>
<nav class="chapter-nav" aria-label="Navegación entre capítulos">{''.join(n)}</nav></main>'''
    return page_shell(post["title"], f'{post["title"]} · Bitácora original del viaje del Atlantis.', body)

def timeline_index(posts):
    sections = []
    for group, idxs in GROUPS:
        cards = []
        for i in idxs:
            p = posts[i]
            cards.append(f'''<article class="timeline-card"><p class="timeline-date">{p["date"]}</p><h3>{esc(p["title"])}</h3>
<p>Relato original escrito durante la travesía.</p><a href="./{p["slug"]}.html">Leer capítulo →</a></article>''')
        sections.append(f'''<section class="timeline-stage"><header><p class="eyebrow">Etapa</p><h2>{group}</h2></header><div class="timeline-grid">{''.join(cards)}</div></section>''')
    body = f'''<main class="shell" id="contenido"><section class="page-hero logbook-hero"><p class="eyebrow">Archivo de viaje · 2021–2022</p><h1>La bitácora completa</h1>
<p class="lead">Dieciséis relatos escritos durante el viaje, ordenados cronológicamente y reunidos aquí sin neutralizar la voz con la que fueron escritos.</p>
<div class="logbook-meta"><span>16 entradas originales</span><span>Noviembre 2021 – Enero 2022</span><span>Buenos Aires → Antártida</span></div></section>
<section class="logbook-note"><p class="eyebrow">Criterio editorial</p><h2>El texto sigue siendo el del viaje</h2>
<p>La web organiza y presenta los relatos; no los reescribe. Se corrigen únicamente errores objetivos y se conserva un enlace a cada publicación original de Blogger.</p></section>
{''.join(sections)}
<section class="route-strip"><p class="eyebrow">Ruta general</p><p>Buenos Aires · Mar del Plata · Rawson · Caleta Hornos · Puerto Deseado · San Julián · Isla de los Estados · Canal Beagle · Ushuaia · Pasaje Drake · Isla Decepción · Gerlache · Bahía Paraíso · Islas Melchior · Canal Murature · regreso por el Drake</p></section></main>'''
    return page_shell("Bitácora", "Bitácora cronológica completa del viaje del velero Atlantis.", body)

def tripulacion_page(post):
    body = f'''<main class="shell" id="contenido"><section class="page-hero"><p class="eyebrow">Los de dos piernas</p><h1>La tripulación</h1>
<p class="lead">Los integrantes del viaje presentados con el texto que fue escrito mientras la expedición estaba en marcha.</p></section>
<article class="journal-entry card"><div class="journal-entry-body">{post["content"]}</div>
<footer class="journal-source"><a href="{esc(post["url"])}" target="_blank" rel="noopener noreferrer">Ver publicación original en Blogger ↗</a></footer></article></main>'''
    return page_shell("Tripulación", "La tripulación del Atlantis presentada con el texto original del viaje.", body, "tripulacion", 1)

def atlantis_page():
    body = '''<main class="shell" id="contenido"><section class="page-hero"><p class="eyebrow">El protagonista</p><h1>Atlantis</h1>
<p class="lead">El barco alrededor del cual se organizaron años de preparación y la expedición hacia las aguas australes.</p></section>
<section class="boat-profile card"><img src="../assets/images/perfil-atlantis.jpg" alt="Vista lateral del velero Atlantis">
<div><p class="eyebrow">Ficha del barco</p><h2>Un velero preparado para el sur</h2>
<p>El Atlantis es un velero de 50 pies de eslora, diseñado por Horacio Escurra para navegar aguas australes y polares. Fue terminado en 2011 por Juan María “Pichín” Broeders y posee casco de acero naval.</p>
<dl class="specs"><div><dt>Eslora</dt><dd>50 pies</dd></div><div><dt>Casco</dt><dd>Acero naval</dd></div><div><dt>Orza</dt><dd>Lastrada · 2 t</dd></div><div><dt>Calado</dt><dd>1,10–3,75 m</dd></div></dl>
<p class="mini-note">Esta página se irá completando con historia del barco, modificaciones, equipamiento y fotografías técnicas.</p></div></section></main>'''
    return page_shell("El Atlantis", "Historia y ficha del velero Atlantis.", body, "atlantis", 1)

def rewrite_nav_file(path, current, prefix):
    if not path.exists(): return
    text = path.read_text(encoding="utf-8")
    replacement = nav(prefix, current)
    text = re.sub(r'<nav class="nav"[^>]*>.*?</nav>', replacement, text, count=1, flags=re.S)
    if path.name == "index.html":
        text = text.replace('href="#historia">Leer la historia</a>', 'href="./pages/bitacora/index.html">Leer la bitácora</a>')
    path.write_text(text, encoding="utf-8")

def main():
    req = Request(FEED, headers={"User-Agent":"AtlantisBitacora/1.0"})
    with urlopen(req, timeout=30) as r:
        feed = json.load(r)
    entries = list(reversed(feed.get("feed", {}).get("entry", [])))
    if len(entries) != 16:
        raise SystemExit(f"Se esperaban 16 entradas y llegaron {len(entries)}")
    posts = []
    for i, e in enumerate(entries):
        posts.append({
            "title": e.get("title",{}).get("$t","").strip(),
            "date": e.get("published",{}).get("$t","")[:10],
            "url": alternate(e),
            "slug": SLUGS[i],
            "content": clean_content(e.get("content",{}).get("$t","")),
        })
    posts[1]["title"] = "La previa"
    posts[5]["title"] = "Los de dos piernas. La tripulación"
    posts[8]["title"] = "Un día explosivo"
    posts[12]["title"] = "San Julián. Club Náutico El Delfín"

    bdir = ROOT / "pages" / "bitacora"
    bdir.mkdir(parents=True, exist_ok=True)
    (bdir / "index.html").write_text(timeline_index(posts), encoding="utf-8")
    for i, post in enumerate(posts):
        (bdir / f'{post["slug"]}.html').write_text(post_page(post, i, posts), encoding="utf-8")
    (ROOT / "pages" / "tripulacion.html").write_text(tripulacion_page(posts[5]), encoding="utf-8")
    (ROOT / "pages" / "atlantis.html").write_text(atlantis_page(), encoding="utf-8")

    css = r'''
/* Bitácora cronológica */
.chapter-hero{max-width:980px;padding-bottom:1.6rem}.journal-entry{max-width:900px;margin:0 auto 2rem;padding:clamp(1.4rem,4vw,3.1rem)}.journal-entry-body{font-family:Georgia,"Times New Roman",serif;font-size:1.06rem;line-height:1.82;color:#263b42}.journal-entry-body p,.journal-entry-body div{margin:0 0 1.05rem}.journal-entry-body img{display:block;max-width:100%;width:auto;height:auto;margin:1.5rem auto;border-radius:16px;box-shadow:var(--shadow-sm)}.journal-entry-body iframe,.journal-entry-body video{display:block;width:100%!important;max-width:100%;height:auto!important;aspect-ratio:16/9;margin:1.5rem auto;border:0;border-radius:14px;overflow:hidden}.journal-entry-body table{display:block;max-width:100%;overflow-x:auto}.journal-entry-body a{color:var(--sea);text-underline-offset:3px}.journal-source{display:flex;flex-wrap:wrap;justify-content:space-between;gap:.7rem;margin-top:2.2rem;padding-top:1rem;border-top:1px solid var(--line);color:var(--ink-soft);font-size:.88rem}.journal-source a{color:var(--navy);font-weight:800}.chapter-nav{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;max-width:900px;margin:0 auto 5rem}.chapter-nav a{display:grid;gap:.2rem;padding:1rem 1.15rem;border:1px solid var(--line);border-radius:var(--radius-sm);background:var(--paper-2);text-decoration:none}.chapter-nav a span{color:var(--sea);font-size:.76rem;font-weight:800;text-transform:uppercase;letter-spacing:.1em}.chapter-nav a strong{font-family:Georgia,"Times New Roman",serif;color:var(--navy)}.timeline-stage{padding:1.25rem 0 3.3rem}.timeline-stage>header{display:grid;grid-template-columns:.33fr 1fr;gap:1.5rem;align-items:end;margin-bottom:1.25rem;border-bottom:1px solid var(--line);padding-bottom:1rem}.timeline-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}.timeline-card{padding:1.35rem;border:1px solid var(--line);border-radius:var(--radius-sm);background:rgba(255,255,255,.72)}.timeline-date{margin-bottom:.55rem;color:var(--rust);font-size:.76rem;font-weight:800;letter-spacing:.1em}.timeline-card h3{font-size:1.3rem}.timeline-card p:not(.timeline-date){margin-top:.7rem;color:var(--ink-soft);font-size:.94rem}.timeline-card a{display:inline-block;margin-top:.9rem;color:var(--navy);font-weight:800}.route-strip{margin:0 0 5rem;padding:1.5rem;border-top:1px solid var(--line);border-bottom:1px solid var(--line);color:var(--ink-soft)}.boat-profile{display:grid;grid-template-columns:minmax(320px,.9fr) minmax(0,1.1fr);gap:2rem;max-width:1000px;margin-bottom:5rem;padding:1.2rem}.boat-profile>img{width:100%;height:100%;min-height:430px;object-fit:cover;border-radius:18px}.boat-profile>div{padding:1rem 1rem 1rem 0}.boat-profile p:not(.eyebrow):not(.mini-note){margin-top:1rem;color:var(--ink-soft)}@media(max-width:900px){.boat-profile,.timeline-stage>header{grid-template-columns:1fr}.boat-profile>img{min-height:0;aspect-ratio:16/10}.boat-profile>div{padding:1rem}.journal-entry-body{font-size:1rem}}@media(max-width:640px){.timeline-grid,.chapter-nav{grid-template-columns:1fr}.journal-entry{padding:1.1rem}.journal-entry-body{font-size:.98rem;line-height:1.74}}
'''
    (ROOT/"css"/"bitacora.css").write_text(css.strip()+"\n", encoding="utf-8")

    rewrite_nav_file(ROOT/"index.html", "inicio", "./")
    rewrite_nav_file(ROOT/"pages"/"gallery.html", "galeria", "../")
    rewrite_nav_file(ROOT/"pages"/"about.html", "about", "../")
    rewrite_nav_file(ROOT/"pages"/"contact.html", "", "../")

if __name__ == "__main__":
    main()
