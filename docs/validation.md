# Revision validation

The redesigned iteration is now grounded in a successful live crawl. See `live-audit-and-gap-analysis.md` and `live-crawl-evidence.json` for source evidence and the comparison with the first design.

## Completed checks

- `python scripts/build.py`: generated ten standalone HTML pages, sitemap and robots.txt. Generated files are committed for direct browsing without a build.
- `python scripts/check_static.py`: passed. All local page/asset targets, anchors, unique IDs, one h1 per page, metadata, external-link security, sitemap XML, EclipseSME identifier isolation, legacy privacy URL compatibility and original-logo byte integrity.
- JavaScript syntax checks passed for config.js, site.js and consent.js. Python scripts compile.
- `python scripts/check_browser.py`: **249 assertions passed** with installed Chromium/Playwright. All provider requests were intercepted or stubbed; no real inquiries or analytics events were sent.
- Ten pages at widths 1440, 1024, 768, 390 and 320px: successful loads, no horizontal overflow, correct desktop/mobile navigation and Escape behavior. FAQ disclosure works; no page JS errors observed.
- Original 202×88 logo loads at its native aspect ratio. Existing 800×534 image loads; all form controls have browser-recognized labels.
- Local explicit success/error simulation, trimming and preserved data. Public development mode and missing/invalid production configuration fail closed. Required field/phone/SMS validation, multiple contact preferences, no-preference rejection, honeypot rejection, CAPTCHA load failure, confirmed success, ambiguous response, malformed JSON, 429, network failure, data preservation, received-state lock and retry cooldown passed.
- Consent tests passed: zero pre-consent requests, blank ID remains inactive, rejection persists, footer focus handling, mocked provider loads once only on acceptance, canonical-only page-view parameters, withdrawal and cookie removal, invalid/expired/future state, cross-tab revocation, blocked browser storage.
- Desktop/mobile full-page screenshots of homepage, services and contact inspected. Corrected photo/grid intrinsic sizing and service-card overflow on narrow phones. Updated foreground colours on vivid-blue diagram layers and the contact band for readability. Screenshots and logs remain local review artifacts, not public site assets.

## Accessibility and performance approach

Semantic landmarks, skip link, one h1, descriptive original-logo alt text, explicit/wrapping form labels, required indicators, browser validation, accessible live status feedback, keyboard navigation and native FAQ details. Visible focus, reduced-motion support, layout reflow and no interaction-gated content. Consent is non-modal and never traps keyboard focus.

Brand accents preserve exact source values. Primary text on white/pale surfaces uses darker blues; white CTA body text is on a deep blue background rather than the vivid turquoise accent. Core text contrast checks are recorded below. Logo typography is preserved as an original brand asset, not recoloured for contrast. No full WCAG certification or screen-reader/device audit is claimed.

Local fonts, classic deferred JS, CSS illustration, native lazy-loaded supporting image, and no framework or runtime font/image service. The original supporting PNG is approximately 549KB and is loaded below the fold; the header logo is under 8KB. No Lighthouse score is claimed.

## Remaining limits

- Managed Chromium blocks `file:` navigation. Relative explicit index paths, local classic scripts, self-hosted assets, and no module/fetch-based page loading support File Explorer browsing; static path checks pass. Reviewer should confirm direct opening in their own browser. No browser security policy was bypassed.
- Real Formspree delivery, CAPTCHA account configuration and GA4 property behavior cannot be verified without the owner's separate identifiers. All remain intentionally blank and production delivery stays unavailable by default.
- Privacy copy needs confirmation against current business practices, retention and request handling. The published WordPress privacy/cookie pages were audited, but stale WordPress/plugin/shopping descriptions are not reproduced as current behavior.
- No Hostinger settings, live redirects, response headers, production 404 status, Safari/Firefox or real-device tests, deployment, WordPress mutation or EclipseSME repository mutation performed.

## Core text contrast calculations

- `#112e3c` on `#ffffff`: 14.19:1
- `#506572` on `#ffffff`: 6.09:1
- `#506572` on `#f0f6f8`: 5.58:1
- `#07688b` on `#f0f6f8`: 5.72:1
- `#002539` on `#13a8ff`: 6.10:1
- `#002539` on `#219ebc`: 5.05:1
- `#ffffff` on `#023047`: 13.85:1
- `#edfaff` on `#07516b`: 8.22:1

These calculations cover named solid-colour text pairs, not an exhaustive rendered-state audit.
