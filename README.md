# EclipseIQ corporate website

A static corporate website with a new editorial design direction, grounded in the verified live EclipseIQ content audit. HTML, CSS and classic JavaScript; no runtime framework or package installation required.

## Review locally
Extract the review archive and open `index.html` from File Explorer. Internal links use explicit relative `index.html` paths. Fonts, original logo and supporting image are self-hosted. Local contact submissions are clearly marked simulations and never reach Formspree. Browser storage persistence on file origins can vary.

Or run from this directory:

```
python -m http.server 4173
```

Then visit http://localhost:4173.

## What is included
- Original corporate logo unchanged, verified blue/turquoise brand colours, and a new self-hosted Manrope typography system.
- An editorial homepage with a keyboard-operable service explorer, complete capability index and distinct EclipseSME software feature.
- Three service practice chapters with native expandable details; a company/leadership narrative; searchable FAQ; contact intake studio; documentary privacy notice.
- All eight verified offerings, all 14 FAQ topics, canonical/social metadata and legacy privacy/cookie URLs preserved.
- Progressive enhancement: all explorer content, navigation and native disclosures work without JavaScript.
- Safe contact simulation, production fail-closed configuration, optional reCAPTCHA and consent-gated GA4 preparation.
- No card grid, stock photograph, stacked-layer illustration, gradients, framework or runtime asset services.

## Maintain
Shared templates: `scripts/build.py`; verified page metadata, offerings and FAQ content: `scripts/content.json`; contact/privacy content: `scripts/partials/*.tpl`. Run `python scripts/build.py` after editing; generated HTML is checked in and directly browsable. Styles and classic scripts live in `assets/`. Public form and analytics configuration lives in `assets/config.js`; never add private credentials.

Checks:

```
python scripts/check_static.py
node --check assets/config.js
node --check assets/site.js
node --check assets/consent.js
```

Browser checks need Playwright and Chromium: start the local server, then run `python scripts/check_browser.py`. Providers are mocked, so no real inquiries or analytics events are sent. Optional share-card regeneration uses `python scripts/social.py`, also with Playwright/Chromium; it composes the unmodified actual logo and local fonts. These tools are not needed to view or host the site.

## Evidence and launch
Start with `docs/creative-direction.md` for the critical assessment, reference research and new design system. Use `docs/live-audit-and-gap-analysis.md` for the live crawl, exact brand values, content inventory and comparison with the first redesign. `docs/live-crawl-evidence.json` records request results and source-file hashes; `docs/assets.md` records asset provenance.

See `docs/configuration.md`, `docs/redirects.md`, `docs/validation.md` and `docs/launch.md`. EclipseIQ's own Formspree endpoint, optional public CAPTCHA key and optional GA4 ID remain unconfigured. The original corporate logo is now included; no temporary branding remains.

This feature branch is for local review. Nothing is deployed, WordPress remains untouched and the EclipseSME repository is unchanged.
