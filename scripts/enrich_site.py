#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

DESCRIPTIONS = {
    "introduccion": "El punto de partida: por qué escribir el viaje mientras todavía está sucediendo.",
    "la-previa": "Años de preparación, cursos, millas navegadas, amigos y la elección del Atlantis.",
    "la-despedida": "La última reunión antes de zarpar: amigos, música y el clima de una partida largamente esperada.",
    "la-meteorologia": "Una historia personal donde medicina, navegación y meteorología terminan cruzándose.",
    "salida-a-mar-del-plata": "La salida desde Núñez y la primera pierna de la travesía hacia Mar del Plata.",
    "la-tripulacion": "Los de dos piernas: presentación de quienes hicieron posible y compartieron la travesía.",
    "de-mdq-a-los-bramadores": "Mar del Plata queda atrás y el Atlantis empieza a ganar sur entre decisiones de ruta y meteorología.",
    "los-pagos-a-eolo": "El viento obliga a cambiar planes y la navegación conduce a Rawson, con nuevas ayudas en el camino.",
    "un-dia-explosivo": "Una de las historias más desopilantes del viaje, ocurrida todavía en Mar del Plata.",
    "caleta-hornos": "Fondeo, exploración y vida a bordo en uno de los refugios naturales de la costa patagónica.",
    "golfo-san-jorge": "Cruce del golfo, fauna, problemas mecánicos y llegada a Puerto Deseado.",
    "altas-latitudes-navegando-los-80": "Un interludio íntimo dedicado a la familia mientras el viaje continúa hacia el sur.",
    "san-julian-club-nautico-el-delfin": "Escala, reparaciones e inolvidable hospitalidad en el Club Náutico El Delfín de San Julián.",
    "50-rugientes-y-dionisio": "La entrada en los 50 Rugientes, Isla de los Estados, Le Maire y la aproximación al Canal Beagle.",
    "ushuaia": "Llegada al Fin del Mundo, preparación del barco y organización de la etapa antártica.",
    "drake-antartida-y-60-rugientes": "El diario completo de la expedición antártica: Drake, fondeos, hielo, Melchior y regreso.",
}

PHOTO_ASSOCIATIONS = {
    "la-previa.html": (
        "../../assets/images/provisiones-muelle.jpg",
        "Preparativos y logística",
        "Parte de la preparación material del viaje: provisiones, organización y trabajo antes de zarpar.",
    ),
    "la-despedida.html": (
        "../../assets/images/brindis-a-bordo.jpg",
        "La previa a bordo",
        "Un brindis entre amigos en los días previos a la partida.",
    ),
    "la-tripulacion.html": (
        "../../assets/images/tripulacion-cubierta.jpg",
        "Tripulación sobre cubierta",
        "Parte del grupo reunido a bordo del Atlantis.",
    ),
    "de-mdq-a-los-bramadores.html": (
        "../../assets/images/atlantis-navegando.jpg",
        "Atlantis en navegación",
        "El barco en el mar durante la travesía hacia el sur.",
    ),
}


def enrich_timeline():
    path = ROOT / "pages" / "bitacora" / "index.html"
    text = path.read_text(encoding="utf-8")
    for slug, description in DESCRIPTIONS.items():
        pattern = re.compile(
            rf'(<article class="timeline-card">.*?<a href="\./{re.escape(slug)}\.html">)',
            re.S,
        )
        match = pattern.search(text)
        if not match:
            continue
        card = match.group(1)
        card = card.replace(
            '<p>Relato original escrito durante la travesía.</p>',
            f'<p>{description}</p>',
            1,
        )
        text = text[:match.start(1)] + card + text[match.end(1):]
    text = text.replace(
        '<a href="./drake-antartida-y-60-rugientes.html">Leer capítulo →</a>',
        '<a href="./antartida/index.html">Explorar la etapa antártica →</a>',
    )
    path.write_text(text, encoding="utf-8")


def photo_block(src, title, caption):
    return f'''<figure class="chapter-photo context-photo"><img src="{src}" alt="{title}"><figcaption><strong>{title}</strong><span>{caption}</span></figcaption></figure>'''


def insert_chapter_photos():
    base = ROOT / "pages" / "bitacora"
    for filename, (src, title, caption) in PHOTO_ASSOCIATIONS.items():
        path = base / filename
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if 'class="chapter-photo context-photo"' in text:
            continue
        marker = '<footer class="journal-source">'
        if marker in text:
            text = text.replace(marker, photo_block(src, title, caption) + marker, 1)
            path.write_text(text, encoding="utf-8")

    # The standalone crew page reuses the same verified crew image.
    path = ROOT / "pages" / "tripulacion.html"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if 'class="chapter-photo context-photo"' not in text:
            marker = '<footer class="journal-source">'
            block = photo_block('../assets/images/tripulacion-cubierta.jpg', 'Tripulación sobre cubierta', 'Parte del grupo reunido a bordo del Atlantis.')
            text = text.replace(marker, block + marker, 1)
            path.write_text(text, encoding="utf-8")


def enrich_home():
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    # Make the primary CTA narrative rather than purely photographic.
    text = text.replace('href="./pages/gallery.html" class="button">Ver la galería</a>', 'href="./pages/bitacora/index.html" class="button">Leer la bitácora</a>')
    text = text.replace('href="#historia">Leer la historia</a>', 'href="./pages/bitacora/index.html">Leer la bitácora</a>')

    if 'class="journey-overview"' not in text:
        section = '''
<section class="journey-overview shell" aria-labelledby="ruta-viaje">
  <div class="journey-heading"><div><p class="eyebrow">Un viaje, cinco etapas</p><h2 id="ruta-viaje">De Buenos Aires a la Antártida</h2></div><p>Los textos escritos durante la travesía ahora forman una bitácora cronológica. Cada etapa reúne relatos, fotografías y la publicación original de Blogger.</p></div>
  <div class="journey-cards">
    <a class="journey-card" href="./pages/bitacora/index.html"><span>01</span><strong>Preparativos</strong><small>La previa, la despedida y todo lo que hizo posible zarpar.</small></a>
    <a class="journey-card" href="./pages/bitacora/index.html"><span>02</span><strong>Rumbo al Sur</strong><small>Mar del Plata, Rawson y las primeras decisiones de una navegación larga.</small></a>
    <a class="journey-card" href="./pages/bitacora/index.html"><span>03</span><strong>Patagonia Austral</strong><small>Caleta Hornos, Golfo San Jorge, Puerto Deseado y San Julián.</small></a>
    <a class="journey-card" href="./pages/bitacora/ushuaia.html"><span>04</span><strong>Fin del Mundo</strong><small>Ushuaia y los últimos preparativos antes del Drake.</small></a>
    <a class="journey-card journey-card-featured" href="./pages/bitacora/antartida/index.html"><span>05</span><strong>Antártida</strong><small>Drake, Isla Decepción, Gerlache, Bahía Paraíso y las Islas Melchior.</small></a>
  </div>
</section>
'''
        anchor = '<section class="video-section">'
        if anchor in text:
            text = text.replace(anchor, section + anchor, 1)
        else:
            text = text.replace('</main>', section + '</main>', 1)
    path.write_text(text, encoding="utf-8")


def append_styles():
    path = ROOT / "css" / "bitacora.css"
    text = path.read_text(encoding="utf-8")
    marker = '/* Third-phase visual integration */'
    if marker in text:
        return
    extra = r'''

/* Third-phase visual integration */
.context-photo{margin:2.2rem 0 1rem;overflow:hidden;border:1px solid var(--line);border-radius:20px;background:var(--paper-2)}
.context-photo img{width:100%;max-height:560px;object-fit:cover;margin:0;border-radius:0;box-shadow:none}
.context-photo figcaption{display:grid;gap:.25rem;padding:1rem 1.15rem;font-family:Inter,ui-sans-serif,system-ui,sans-serif}
.context-photo figcaption strong{font-family:Georgia,"Times New Roman",serif;color:var(--navy);font-size:1.08rem}
.context-photo figcaption span{color:var(--ink-soft);font-size:.9rem}
.journey-overview{padding:2rem 0 5rem}.journey-heading{display:grid;grid-template-columns:1fr minmax(280px,.7fr);gap:2rem;align-items:end;margin-bottom:1.4rem}.journey-heading>p{color:var(--ink-soft)}
.journey-cards{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:.8rem}.journey-card{display:grid;align-content:start;gap:.45rem;min-height:190px;padding:1.15rem;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.72);text-decoration:none;transition:transform .2s ease,box-shadow .2s ease}.journey-card:hover{transform:translateY(-3px);box-shadow:var(--shadow-sm)}.journey-card>span{color:var(--rust);font-size:.72rem;font-weight:800;letter-spacing:.12em}.journey-card strong{font-family:Georgia,"Times New Roman",serif;color:var(--navy);font-size:1.15rem}.journey-card small{color:var(--ink-soft);font-size:.85rem;line-height:1.5}.journey-card-featured{background:var(--navy);border-color:var(--navy)}.journey-card-featured strong,.journey-card-featured small,.journey-card-featured span{color:#fff}
@media(max-width:1000px){.journey-cards{grid-template-columns:repeat(2,minmax(0,1fr))}.journey-card-featured{grid-column:1/-1}.journey-heading{grid-template-columns:1fr}}
@media(max-width:640px){.journey-cards{grid-template-columns:1fr}.journey-card-featured{grid-column:auto}.journey-card{min-height:0}}
'''
    path.write_text(text + extra, encoding="utf-8")


def main():
    enrich_timeline()
    insert_chapter_photos()
    enrich_home()
    append_styles()


if __name__ == '__main__':
    main()
