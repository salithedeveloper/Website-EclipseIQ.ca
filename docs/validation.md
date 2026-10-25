# Validation: production contact integration

## Completed checks

- **323 Chromium browser assertions passed** across 1440, 1024, 768, 390 and 320px. All 11 active pages loaded without horizontal overflow. Mobile menu, Escape, desktop navigation, no-JavaScript navigation, native FAQ disclosures and reduced motion were verified.
- New navigation destinations are Products, Services, About, FAQ and Contact. Both homepage business-area entry points open their correct destination. The four offerings remain in the required order; implementation/integration of third-party software is explicit.
- All homepage images decoded successfully, including lazy assets. The self-hosted IBM Plex Sans font loaded successfully. Desktop/mobile full-page screenshots were inspected for Home, Products, Services, About, FAQ and Contact.
- The product catalogue still publishes only EclipseSME. The disposable catalogue regression test confirms draft products stay absent and an explicitly published second product uses the same shared layout. No unreleased product is named publicly.
- Static checks cover all 11 active HTML files: one H1, unique IDs, titles/descriptions/canonicals, local references/fragments, external-link security, public email absence, sitemap, policy aliases and unchanged original-logo hash.
- JavaScript syntax checks pass for config, site and consent scripts. The supplied public production settings and CAPTCHA handling are covered by dedicated tests. HTML/CSS, contact controls, consent code and the analytics setting remain unchanged.
- Form tests retain required fields, trimming, email/phone/SMS preferences, conditional phone validation, honeypot, optional CAPTCHA failure, local simulated success/error, mocked production success/failure and retry/duplicate prevention. Unconfigured production and forced submit events cannot send a request or report success.
- Consent tests retain no pre-consent analytics, persisted rejection, explicit acceptance, sanitized page data, withdrawal, expiry, invalid state, cross-tab changes and blocked browser storage. All provider traffic was intercepted: no real inquiry or analytics was sent.

## Review and limits

The actual root `index.html` remains directly browsable using explicit relative local paths. Browser QA uses a local HTTP server because this execution environment restricts direct `file:` browser navigation. Captures remain in ignored `.test-results/`; no review folder was created.

New editorial imagery is illustrative. Product images are explicitly labelled as concepts, not live application screenshots. They do not imply customer results, employee identities or actual office premises.

The dedicated Formspree endpoint and public v2 key are now configured. Added checks verify the committed hosted configuration, checkbox rendering and responsive size, unchecked/expired/error states, token payload, pending/duplicate protection, HTTP/JSON confirmation and rejected responses. Ordinary local production-config previews simulate without contacting providers. Explicit local opt-in exercises the delivery path with intercepted providers. The opt-in preview server was also checked over loopback: only its served config enables real delivery; repository config remains safe.

No real inquiry was sent. Google hostname permissions, Formspree private setup and actual recipient delivery need the manual test in `docs/configuration.md`. Optional analytics remains unconfigured. Nothing is deployed; WordPress and the EclipseSME repository remain unchanged.
