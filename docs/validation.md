# Validation: products-and-services website

## Scope

Eleven active HTML files: Home, Products, Our Offerings, Company, FAQ, Contact, canonical privacy, three compatibility privacy/cookie URLs and 404. Historical concepts are excluded from production checks.

## Completed checks

- Static checks: unique IDs, one H1, page titles, descriptions and canonical URLs, local asset/link existence, fragment targets, external-link safety, public email absence, sitemap, original-logo hash and legacy policy aliases.
- JavaScript syntax checks for config, site and consent scripts.
- Chromium browser suite: **284 assertions passed** across 1440, 1024, 768, 390 and 320px. All active pages loaded without horizontal overflow. Desktop/mobile navigation, Escape behaviour, current-page Products navigation, product/demo discovery, exact offering order and grouped FAQ counts were verified.
- Catalogue growth regression test in a disposable directory: an unpublished fixture is absent from Home and Products; explicitly publishing it renders a second feature through the existing layout, without touching production files.
- Products check: only one product is published, EclipseSME. Homepage shows the four requested offerings in order. FAQ and Products are visible in the primary navigation; the homepage includes three expandable FAQ answers.
- Navigation and native disclosures work without JavaScript, including mobile layouts. Reduced-motion preference disables smooth scrolling.
- Form tests retain required-field checks, trimming, contact preferences, conditional phone, honeypot, CAPTCHA failure, local simulation, provider success/failure and duplicate/retry prevention. Unconfigured production and forced submit events cannot send a request or report success.
- Cookie/analytics tests retain no pre-consent requests, stored rejection, explicit acceptance, sanitized page data, withdrawal, expiry, invalid state, cross-tab rejection and blocked storage handling. All providers are intercepted; no real inquiry or analytics is sent.
- Desktop/mobile homepage screenshots and primary interior-page screenshots inspected. Captures remain in ignored `.test-results/`, not a new review folder.

The source and generated pages use explicit relative paths for direct local opening of root `index.html`. Browser QA uses a local HTTP server because this execution environment restricts direct browser `file:` navigation.

## Publication limits

Live Formspree delivery awaits a dedicated EclipseIQ endpoint. Optional analytics remains unconfigured. No deployment, live WordPress modification or EclipseSME repository change is included.
