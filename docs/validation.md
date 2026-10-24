# Creative-reset validation

## Scope

New homepage composition and visual hierarchy; a new self-hosted display/body font system; three practice chapters for the eight source offerings; company/leadership narrative; searchable FAQ; compact contact studio; readable privacy document. Original logo, factual content, metadata, form/consent safeguards and legacy paths retained. See `creative-direction.md` for the critique and research.

## Checks completed

- Generated all ten standalone pages; local link/asset targets, fragments, duplicate IDs, one h1, titles/descriptions/canonicals, external-link security, sitemap, identifier isolation and legacy privacy compatibility pass static checks.
- Original-logo SHA-256 remains `e9edbbf8165884a95bdbf18d2a7007b911fbaf35306d39c65a42bb1036b4b9fd`.
- JS syntax and Python compile checks pass.
- **262 browser assertions passed** using installed Chromium/Playwright, local HTTP and fully intercepted provider test scenarios. No real Formspree submission or analytics event sent.
- All ten pages at 1440, 1024, 768, 390 and 320px: no horizontal overflow, working mobile navigation/Escape behavior, correct desktop toggle visibility and no JS exceptions.
- Service explorer: one selected pathway, content/selection/focus updates on arrow keys, Home/End support, real service links, and all three content paths available without JavaScript.
- Direct service links open the correct disclosure. Native service/FAQ disclosures and navigation work without JavaScript. FAQ search filters answer content, announces counts, handles empty state and restores all 14 topics when cleared. Reduced motion disables smooth scrolling.
- Original-logo loading and programmatic form labels checked. Contact success/error simulation, conditional phone/SMS requirements, multiple contact preferences, no-preference/honeypot rejection, unconfigured public fail-closed behavior, required CAPTCHA failure, provider success/ambiguous/malformed/429/network responses, data preservation and resend controls pass.
- Consent: zero pre-consent traffic, empty GA ID stays inactive, stored rejection, focus handling, mocked provider loading after acceptance only, canonical-only page-view data, withdrawal/reload/cookie removal, invalid/expired/future choices, cross-tab revocation and blocked storage pass.
- Homepage, services, company and contact full-page screenshots inspected at desktop and mobile widths. New layout is typography-led, without the old stock photo, card grid, layered illustration or gradients. Actual quality remains subject to owner review; tests do not certify aesthetics.

## Accessibility and performance

Semantic landmarks, skip link, native disclosures, ARIA tab/tabpanel relationships, roving tab focus, visible focus styles, explicit/wrapping form labels, browser constraints, live feedback and reduced-motion support. No scroll-jacking, autoplay, animated backdrop or content gated behind motion. All explorer content is present in static HTML and visible without JavaScript.

The new main font is approximately 25KB, and the original logo is under 8KB. No below-fold stock image, framework, external font service or external image dependency. No performance score or WCAG certification claimed. Core text contrast pairs are recorded below; this is not a complete assistive-technology audit.

## Limits before launch

Managed Chromium blocks `file:` navigation. Explicit relative index paths, classic local scripts and fully local assets remain in place; reviewer should confirm File Explorer opening in their own browser. Real provider account configuration and delivery require EclipseIQ's own identifiers, which remain blank. Privacy/business retention practices still need owner confirmation. Hostinger headers, production redirects/404 status, real devices, Safari/Firefox and live integration behavior remain outside this local review. No deployment, WordPress change or EclipseSME repository mutation performed.

## Core text contrast calculations

- `#071f2c` on `#f3f2ee`: 15.10:1
- `#54646b` on `#f3f2ee`: 5.49:1
- `#b1c5d0` on `#071f2c`: 9.48:1
- `#13a8ff` on `#071f2c`: 6.50:1
- `#435f6c` on `#ffffff`: 6.79:1
- `#0876a4` on `#ffffff`: 5.08:1
- `#446675` on `#dceef5`: 5.17:1
- `#a8bfcb` on `#071f2c`: 8.84:1
