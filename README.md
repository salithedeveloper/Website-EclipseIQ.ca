# EclipseIQ corporate website

A concise static corporate website for EclipseIQ Technologies Inc. The content starts with the live corporate site's insurance software, consulting and senior leadership positioning. No framework or package installation is required.

## Review locally

Run `git pull` on `feat/eclipseiq-website-redesign`, then open the root `index.html` in a browser. Relative links include explicit `index.html` filenames; the original logo, font and photograph are local. No build step is needed.

Alternatively, run `python -m http.server 4173` in this directory and open http://localhost:4173.

## Site structure

- Home: company positioning, three service summaries, EclipseSME product section, company introduction and contact link.
- Services: consulting, engineering/modernization, fractional leadership and software, plus concise audit readiness, security and coaching support.
- Company: insurance experience, audiences and engagement options.
- Contact: existing inquiry form with configurable Formspree delivery; no public email address.
- Common questions: eight short answers, linked from the footer.
- Cookies & privacy: existing consent foundations and compatibility URLs.

Navigation focuses on Services, Company, EclipseSME and Contact. There is no interactive service explorer, abstract capability diagram or FAQ search. The historical `review/homepage-concepts` folder is unchanged and is not part of the active website.

## Maintain

Templates live in `scripts/build.py`; concise page metadata, services and questions live in `scripts/content.json`. Contact and privacy markup live in `scripts/partials/`. After editing these sources, run `python scripts/build.py` and commit the generated HTML as well. The generated root `index.html` is the actual website, not a concept.

Styles and scripts live in `assets/`. Public form/analytics configuration remains in `assets/config.js`. The form currently simulates submissions locally; live delivery requires EclipseIQ's own Formspree endpoint. Optional analytics remains unconfigured and consent-gated. No private keys belong in these files.

## Verification

```sh
python scripts/check_static.py
node --check assets/config.js
node --check assets/site.js
node --check assets/consent.js
```

For browser checks, start the local server and run `python scripts/check_browser.py`. Requires the existing Playwright and Chromium environment. The suite intercepts external providers; it never sends real inquiries or analytics. `ECLIPSEIQ_TEST_URL` can select another local port. Screenshots are saved to ignored `.test-results/`.

See `docs/creative-direction.md`, `docs/assets.md`, `docs/validation.md` and `docs/configuration.md`. This branch is for local review. No deployment or live WordPress changes are included.
