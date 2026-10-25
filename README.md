# EclipseIQ insurance technology products & services

A static corporate website for EclipseIQ Technologies Inc., with proprietary insurance software, implementation and modernization, InsurTech consulting and fractional executive leadership.

## Review locally

On `feat/eclipseiq-website-redesign`, run `git pull` and open root `index.html`. No build step, framework or package installation is needed. Internal links use explicit relative `index.html` filenames; fonts and the original logo are local.

For an HTTP preview, run `python -m http.server 4173` and open http://localhost:4173.

## Website structure

- **Home:** a substantial engineering introduction, equal Products/Services entry points, four ordered offerings, flagship product, company experience and FAQ preview.
- **Products:** a public product catalogue, currently featuring only EclipseSME™, its capabilities and implementation support.
- **Our Offerings:** Insurance Software; Insurance Software Implementation & Modernization; Insurance Technology Consulting; Fractional CIO / COO / CTO Leadership. Audit readiness, security reviews, Totality Assessment and coaching are retained within their practices.
- **Company:** product development, insurance experience and expertise across our own and third-party platforms.
- **FAQ:** nine concise answers in two groups, with native expandable questions.
- **Contact:** the existing configurable inquiry form and contact preferences. No publicly displayed email address.
- **Cookies & privacy:** consent controls and existing compatibility URLs.

## Products and future additions

`scripts/content.json` contains the public product catalogue. Products render only when `published` is explicitly `true`. Each entry supplies its own name, content, links, capabilities and illustrative workflow labels. Both the homepage and Products page use a shared product feature component that accommodates additional released products.

EclipseSME is the only published entry. Unreleased ideas are not displayed; no availability, feature descriptions or launch dates are implied for them. Do not mark a draft published until the owner approves its public content.

## Maintenance

Templates: `scripts/build.py`. Content and metadata: `scripts/content.json`. Contact/privacy markup: `scripts/partials/`. Run `python scripts/build.py` after source edits and commit generated HTML. Root `index.html` remains the actual website.

The visual system is in `assets/styles.css`; navigation, form handling and consent use classic local JavaScript. The original logo is unchanged. Manrope headings and self-hosted IBM Plex Sans body text support a corporate visual system. Commissioned engineering imagery and a clearly labelled product concept render replace the former miniature capability diagrams. They do not depict actual staff, offices or a live product interface. See `docs/enterprise-design-research.md` and `docs/assets.md`. Historical assets and `review/homepage-concepts/` remain unused by the active layouts.

The EclipseIQ Formspree endpoint and public reCAPTCHA v2 checkbox key are configured in `assets/config.js`. HTTPS production inquiries require a completed CAPTCHA and provider-confirmed receipt. Ordinary local/file previews remain explicitly simulated and send no provider requests. For a deliberate real local test, use `python scripts/preview_form_delivery.py --real-delivery --port 4174`; see `docs/configuration.md` for domain/setup prerequisites and the manual test checklist. The secret key stays only in Formspree. Analytics remains unconfigured and unchanged. Automated tests intercept provider traffic and send no real inquiries.

## Checks

```sh
python scripts/check_static.py
python scripts/check_catalog.py
node --check assets/config.js
node --check assets/site.js
node --check assets/consent.js
```

With Playwright and Chromium installed, start the local server and run `python scripts/check_browser.py`. `ECLIPSEIQ_TEST_URL` selects a different port. Screenshots go to ignored `.test-results/`. `scripts/social.py` regenerates the corporate sharing image.

Nothing is deployed. The live WordPress website and EclipseSME repository are unchanged.
