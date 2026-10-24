# Validation — 23 October 2026

## Completed
- Generated all 7 static HTML pages; source and generated output checked in. No build is required to view them.
- `python scripts/check_static.py`: passed. Seven pages, one h1 each, language/title/description/canonical, unique IDs, local page/assets/fragment targets, external-link noopener, XML sitemap, and isolation from EclipseSME analytics identifiers.
- `node --check` on config.js, site.js and consent.js: passed. Python scripts compile.
- `python scripts/check_browser.py`: **187 assertions passed** with installed Chromium and Playwright over the local static server and fully intercepted production/provider scenarios. No actual inquiry or analytics request was sent.
- Every page checked at widths 1440, 1024, 768, 390 and 320px: no horizontal overflow, pages load, desktop menu hidden, mobile menu and Escape behavior work. FAQ disclosure works. No page JavaScript exceptions observed.
- Local form simulation: explicit success/error wording, no provider requests, trimming and preserved test values. Production-like tests: required field validation, conditional phone, empty/invalid configuration, missing required CAPTCHA, failed CAPTCHA load, confirmed provider success, ambiguous success, malformed JSON, HTTP 429, network failure, retained entries and retry cooldown. Only provider-confirmed success resets and locks the form.
- Consent: no external requests before consent, empty GA ID stays inactive even after acceptance, rejection persistence, footer keyboard focus, configured provider loads once only after acceptance, canonical-only page-view data, withdrawal/reload, accessible first-party cookie removal, expired/future/invalid choices, blocked storage and cross-tab revocation. Provider scripts are stubs; these are integration-contract tests, not live Google verification.
- Desktop and mobile full-page screenshots inspected. Corrected desktop menu toggle visibility and replaced unsupported arrow glyphs with inline SVG icons. Screenshots and test logs are local review artifacts excluded from Git.
- No third-party font/image dependency. Runtime assets total roughly 84KB (including PNG share card); generated pages are small standalone documents. No performance score is claimed.

## Accessibility approach
Semantic header/nav/main/footer, skip link, one h1, explicit input labels and required indicators, native form constraints, visible focus styles, live status region and focused feedback, keyboard-operable navigation and FAQ, native details, reduced-motion handling, responsive reflow and no scroll-gated content. Consent is non-modal and does not trap focus. Core palette text contrasts are checked separately below. No screen-reader certification, automated WCAG conformance score or full assistive-device audit claimed.

## Limits / required follow-up
- The managed Chromium administrator policy blocks navigation to `file:` URLs. The architecture deliberately uses explicit relative index.html paths, classic local scripts, no modules, no AJAX content fetching and no external assets. All path targets pass static checks. Direct File Explorer opening still needs reviewer confirmation in their own browser; no browser policy was bypassed.
- Live website access/logo retrieval was incomplete; see discovery.md. Corporate logo remains a clearly labelled placeholder and exact brand values need confirmation. Source public navigation was audited through cached pages, not a complete live crawl.
- No live Formspree endpoint, CAPTCHA key or GA4 ID supplied. Real delivery, real provider account settings and live analytics remain unverified. IDs are intentionally blank.
- No Hostinger headers, redirect configuration, custom domain, 404 HTTP status, real device testing, Safari/Firefox testing or production deployment performed. Server headers and remote privacy settings must be reviewed at launch.

## Core text contrast calculations

- ink on paper: 12.43:1
- muted on paper: 5.64:1
- blue on paper: 5.58:1
- muted on tint: 5.32:1
- blue on tint: 5.26:1
- paper on navy: 13.08:1
- hero secondary on navy: 9.22:1
- turquoise title on navy: 8.99:1

These checks cover the named core pairs, not every rendered element or gradient.
