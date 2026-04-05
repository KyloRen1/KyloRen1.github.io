### Personal website

Built with [Pelican](https://getpelican.com/) - a Python static site generator.

## Setup

### Prerequisites
- Python 3.9+
- `uv` package manager ([install here](https://astral.sh/uv))

### Installation

```bash
# Install dependencies using uv
uv sync

# Build the site
uv run python source/build.py
```

### Local Development

```bash
# Rebuild the site after making changes
uv run python source/build.py

# Serve locally to preview
uv run python -m http.server 8000 --directory .

# Then open http://localhost:8000 in your browser
```

### Project Structure

```
.
├── source/
│   ├── content/
│   │   ├── pages/      # Markdown pages (CV, Reviews, etc.)
│   │   └── static/     # Static files (assets, etc.)
│   ├── theme/          # Jinja2 templates and CSS
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── index.html      # Homepage template
│   │   │   └── page.html
│   │   └── static/
│   │       ├── main.css
│   │       ├── particle-network.js
│   │       └── scroll-nav.js
│   ├── pelicanconf.py  # Pelican configuration
│   └── build.py        # Build script
├── index.html          # Generated homepage
├── cv/                 # Generated CV page
├── reviews/            # Generated Reviews page
└── assets/             # Static assets (copied from source)
```

### Build & Deploy

The site is automatically built and deployed to GitHub Pages via GitHub Actions on every push to `main`.

### Making Changes

1. **Homepage content**: Edit `source/theme/templates/index.html`
2. **Pages (CV, Reviews)**: Edit markdown files in `source/content/pages/`
3. **Styling**: Update `source/theme/static/main.css`
4. **Theme templates**: Modify templates in `source/theme/templates/`

After making changes, run `uv run python source/build.py` to regenerate the site.

### Migrated from Jekyll

This site was migrated from Jekyll to Pelican for:
- Better Python integration
- Easier customization
- Simplified maintenance
- Better control over the build process

The particle animation background and all styling have been preserved.