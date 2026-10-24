# Validation: corporate visual refinement

Completed for the current visual-only revision:

- Exact before/after comparison of all 10 active pages: visible text, text order, metadata, section order and anchor destinations are unchanged. Contact markup, form/consent JavaScript, configuration, content JSON, sitemap and robots.txt remain unchanged.

- Static checks on all 10 active HTML files, excluding historical concepts: unique IDs, one H1, title/description/canonical, local assets and links, fragments, external-link security, sitemap, original-logo hash and legacy privacy aliases.
- JavaScript syntax checks for `config.js`, `site.js` and `consent.js`.
- Chromium browser suite: **257 assertions passed**. All active pages checked at 1440, 1024, 768, 390 and 320px; no horizontal overflow; desktop/mobile navigation and Escape behaviour verified; no page JavaScript errors. Native FAQ and mobile navigation also work without JavaScript.
- Inquiry behaviour: local simulated success/error, required fields, multiple contact preferences, conditional phone requirement, honeypot, mocked provider success/failure, retained entries, resend prevention, missing configuration and optional CAPTCHA.
- Consent behaviour: no pre-consent analytics, rejection persistence, explicit acceptance, sanitized page data, withdrawal, expired/invalid state, cross-tab rejection and blocked browser storage. All external providers were intercepted; no real submission or analytics was sent.
- New service-image click targets verified at 1440, 768, 390 and 320px; each opens the correct existing service anchor. All homepage images decoded successfully at each width.
- Full-page desktop and mobile homepage screenshots inspected, along with Services, Company and Contact. Screenshot output is local and ignored in `.test-results/`; no new review folder is created.

The complete website remains directly browsable from root `index.html` using explicit relative paths. Browser layout tests use a local HTTP server; this execution environment restricts direct `file:` navigation. Static checks validate the file-relative links and assets.

Live form delivery and analytics are not configured or tested against real providers. The existing local simulation remains clearly labelled; the verified support email provides a separate contact route. No deployment or live WordPress changes.
