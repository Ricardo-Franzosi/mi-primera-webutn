# Francho y el Atlantis

Sitio web estático desarrollado originalmente como práctica de HTML y CSS para UTN y convertido progresivamente en una **bitácora digital de navegación** sobre el velero **Atlantis**, su tripulación, los preparativos y la expedición al Fin del Mundo y la Antártida.

## Estado actual

La versión 2026 conserva HTML y CSS sin frameworks innecesarios, pero incorpora una estructura narrativa completa del viaje.

### Mejoras incorporadas

- HTML5 semántico y navegación consistente.
- Diseño responsive para escritorio, tablet y celular.
- Estética inspirada en una bitácora náutica.
- Accesibilidad básica: navegación por teclado, foco visible y enlace para saltar al contenido.
- **16 entradas originales de Blogger** organizadas cronológicamente por etapas.
- Etapa antártica dividida editorialmente en cinco capítulos navegables.
- Páginas independientes de **Tripulación** y **El Atlantis**.
- Galería de fotografías propias y fotografías contextuales dentro de los capítulos.
- Importación automatizada desde el feed público de Blogger.
- Limpieza automática del HTML heredado de Blogger sin reescribir los relatos.
- Uso de variantes de mayor resolución para las imágenes originales del blog.
- Videos responsive, incluyendo la entrevista realizada durante el regreso en el Club Náutico El Delfín de Puerto San Julián.
- Despliegue automático mediante GitHub Pages.

## Estructura principal

```text
mi-primera-webutn/
├── .github/workflows/
├── assets/images/
├── css/
│   ├── styles.css
│   └── bitacora.css
├── pages/
│   ├── bitacora/
│   │   └── antartida/
│   ├── gallery.html
│   ├── tripulacion.html
│   ├── atlantis.html
│   └── about.html
├── scripts/
│   ├── build_bitacora.py
│   ├── split_antartida.py
│   └── enrich_site.py
├── index.html
└── README.md
```

## Publicación

Los cambios incorporados a `main` se despliegan mediante GitHub Pages.

Sitio público:

`https://ricardo-franzosi.github.io/mi-primera-webutn/`

Bitácora:

`https://ricardo-franzosi.github.io/mi-primera-webutn/pages/bitacora/`

Galería:

`https://ricardo-franzosi.github.io/mi-primera-webutn/pages/gallery.html`

## Próximas etapas

- Incorporar nuevas fotografías y videos del archivo del viaje.
- Completar la historia técnica del Atlantis.
- Agregar un mapa o línea temporal geográfica de la travesía.
- Revisar progresivamente el material disponible en otras fuentes públicas del proyecto.

## Autor

Ricardo Franzosi
