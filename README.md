# EclipseIQ corporate website

A static corporate website grounded in a fresh live audit of EclipseIQ.ca. HTML, CSS and classic JavaScript; no runtime framework or package installation required.

## Review locally
Extract the review archive and open `index.html` from File Explorer. Internal links use explicit relative `index.html` paths. Fonts, original logo and supporting image are self-hosted. Local contact submissions are clearly marked simulations and never reach Formspree. Browser storage persistence on file origins can vary.

Or run from this directory:

```
python -m http.server 4173
```

Then visit http://localhost:4173.

## What is included
- Original corporate logo, unchanged from the live WordPress asset; verified blue/turquoise palette and IBM Plex typography.
- Homepage, eight-offering services page, company/expertise page, all 14 FAQ topics, contact and privacy notice.
- Compatibility pages for `/privacy/`, `/cookie-policy-ca/` and `/cookie-policy-ca-2/`, plus a 404 document.
- Self-hosted fonts and existing-site editorial image; no external fonts or image services at runtime.
- AJAX contact flow with safe local simulation, production fail-closed configuration and optional reCAPTCHA v2.
- Stored accept/reject preferences, footer preference control, consent-gated GA4 preparation and withdrawal.
- Canonical/social metadata, actual-logo organization schema, sharing card, sitemap and robots.txt.

## Maintain
Shared templates, offerings and copy: `scripts/build.py`. Run `python scripts/build.py` after editing; generated HTML is checked in and directly browsable. Styles and classic scripts live in `assets/`. Public form and analytics configuration lives in `assets/config.js`; never add private credentials.

Checks:

```
python scripts/check_static.py
node --check assets/config.js
node --check assets/site.js
node --check assets/consent.js
```

Browser checks need Playwright and Chromium: start the local server, then run `python scripts/check_browser.py`. Providers are mocked, so no real inquiries or analytics events are sent. Optional share-card regeneration uses `python scripts/social.py`, also with Playwright/Chromium; it composes the unmodified actual logo and local fonts. These tools are not needed to view or host the site.

## Evidence and launch
Start with `docs/live-audit-and-gap-analysis.md` for the live crawl, exact brand values, content inventory and comparison with the first redesign. `docs/live-crawl-evidence.json` records request results and source-file hashes; `docs/assets.md` records asset provenance.

See `docs/configuration.md`, `docs/redirects.md`, `docs/validation.md` and `docs/launch.md`. EclipseIQ's own Formspree endpoint, optional public CAPTCHA key and optional GA4 ID remain unconfigured. The original corporate logo is now included; no temporary branding remains.

This feature branch is for local review. Nothing is deployed, WordPress remains untouched and the EclipseSME repository is unchanged.
