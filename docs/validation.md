# Validation: corporate visual refinement

Completed for the current visual-only revision:

- Targeted content updates on Home, Company and FAQ; demo link added to the verified https://eclipsesme.com/contact/ page. Public email/mailto links removed from Contact and all privacy aliases. Static checks prohibit public EclipseIQ email addresses in the active HTML. Contact form markup, form/consent JavaScript, configuration, sitemap and robots.txt remain unchanged.

- Static checks on all 10 active HTML files, excluding historical concepts: unique IDs, one H1, title/description/canonical, local assets and links, fragments, external-link security, sitemap, original-logo hash and legacy privacy aliases.
- JavaScript syntax checks for `config.js`, `site.js` and `consent.js`.
- Chromium browser suite: **261 assertions passed**. All active pages checked at 1440, 1024, 768, 390 and 320px; no horizontal overflow; desktop/mobile navigation and Escape behaviour verified; no page JavaScript errors. Native FAQ and mobile navigation also work without JavaScript.
- Demo CTA verified against the product demo URL; eight concise FAQ topics checked.
- Inquiry behaviour: local simulated success/error, required fields, multiple contact preferences, conditional phone requirement, honeypot, mocked provider success/failure, retained entries, resend prevention, missing configuration and optional CAPTCHA.
- Consent behaviour: no pre-consent analytics, rejection persistence, explicit acceptance, sanitized page data, withdrawal, expired/invalid state, cross-tab rejection and blocked browser storage. All external providers were intercepted; no real submission or analytics was sent.
- New service-image click targets verified at 1440, 768, 390 and 320px; each opens the correct existing service anchor. All homepage images decoded successfully at each width.
- Full-page desktop and mobile homepage screenshots inspected, along with Services, Company and Contact. Screenshot output is local and ignored in `.test-results/`; no new review folder is created.

The complete website remains directly browsable from root `index.html` using explicit relative paths. Browser layout tests use a local HTTP server; this execution environment restricts direct `file:` navigation. Static checks validate the file-relative links and assets.

Live form delivery and analytics are not configured or tested against real providers. The existing local simulation remains clearly labelled and is restricted to file/localhost origins. Hosted submission is disabled without valid production configuration; forced submit events also produce no provider request or success message. Inquiries are directed through the contact form; no public email is displayed. No deployment or live WordPress changes.
