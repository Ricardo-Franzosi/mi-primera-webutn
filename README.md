# Francho y el Atlantis

Sitio web estático desarrollado originalmente como práctica de HTML y CSS para UTN. Funciona como una bitácora personal de la preparación y navegación del velero **Atlantis** hacia el Fin del Mundo.

## Estado actual

La versión 2026 moderniza el proyecto original sin cambiar su identidad ni convertirlo en una aplicación innecesariamente compleja.

### Mejoras incorporadas

- HTML5 semántico y válido.
- Navegación consistente entre páginas.
- Diseño responsive para escritorio, tablet y celular.
- Mejor jerarquía visual, legibilidad y contraste.
- Accesibilidad mejorada con navegación por teclado, foco visible y enlace para saltar al contenido.
- Metadatos básicos para SEO y vista previa social.
- Imágenes dimensionadas y carga diferida donde corresponde.
- YouTube con dominio `youtube-nocookie.com`.
- Sin dependencias JavaScript ni framework.
- Sin carga externa de fuentes.
- Favicon SVG liviano.
- Workflow preparado para desplegar automáticamente en GitHub Pages desde `main`.

## Estructura

```text
mi-primera-webutn/
├── .github/
│   └── workflows/
│       └── pages.yml
├── assets/
│   └── favicon.svg
├── css/
│   └── styles.css
├── pages/
│   ├── about.html
│   └── contact.html
├── index.html
└── README.md
```

## Tecnologías

- HTML5
- CSS3
- GitHub Actions
- GitHub Pages
- YouTube Embed

No requiere instalación, compilación ni dependencias. Para verlo localmente basta con abrir `index.html` en un navegador moderno.

## Publicación

El archivo `.github/workflows/pages.yml` está preparado para desplegar el sitio cuando hay cambios en la rama `main`.

En GitHub, la fuente de publicación debe configurarse una vez en:

**Settings → Pages → Build and deployment → Source → GitHub Actions**

Después de esa configuración, cada actualización de `main` dispara automáticamente el despliegue.

La URL esperada del proyecto es:

`https://ricardo-franzosi.github.io/mi-primera-webutn/`

## Próximas mejoras posibles

- Incorporar nuevos capítulos o entradas de la expedición.
- Guardar localmente fotografías actualmente servidas desde Blogger.
- Agregar una galería fotográfica optimizada.
- Incorporar fechas, lugares y una línea temporal de la navegación.
- Añadir un formulario de contacto sólo si realmente resulta necesario.

## Autor

Ricardo Franzosi
