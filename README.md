# EclipseIQ corporate website

Static HTML, CSS and JavaScript. No runtime dependencies, frameworks, cookies from third-party assets, or build step required to view the delivered pages.

## Review locally
Open `index.html` from File Explorer. All navigation uses relative paths with explicit `index.html` filenames, so nested pages work from `file:` and static web hosting. JavaScript uses classic deferred scripts, not modules or fetch-based page loading. Local form submissions are clearly labelled simulations and do not reach Formspree. Your browser may limit preference persistence for file origins.

Alternatively, from this directory:

```
python -m http.server 4173
```

Visit http://localhost:4173. No deployment is needed.

## Maintain
- Edit shared templates and page copy in `scripts/build.py`, then run `python scripts/build.py`. Generated HTML is checked in for direct browsing.
- Edit `assets/styles.css` and the classic scripts directly.
- Public configuration lives in `assets/config.js`. No secret keys belong in this repository.
- `python scripts/check_static.py` validates local paths, anchors, metadata and identifier isolation.
- `node --check assets/site.js` and `node --check assets/consent.js` check JS syntax.
- Optional browser checks: `python scripts/check_browser.py` (Playwright plus installed Chromium; no actual network submissions).
- `assets/social.png` is an original text-only sharing card, not a logo. `scripts/social.py` can regenerate it with Pillow; Pillow is not required to view the site.

## Review before launch
The corporate logo is intentionally a labelled temporary placeholder. Blue/turquoise is preserved as the brand family; exact colour values still need confirmation. Original logo replacement, Formspree configuration and privacy practice review are required before publication. GA4 can remain disabled.

See `docs/discovery.md`, `docs/configuration.md`, `docs/launch.md`, `docs/redirects.md` and `docs/validation.md` for evidence, configuration, limitations and launch steps. The existing WordPress site and EclipseSME repository have not been modified. This branch is for review only; nothing is deployed.
