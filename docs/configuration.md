# Forms, consent and analytics

## Technical reference
Reviewed read-only: `salithedeveloper/Website-EclipseSME.com`, branch `feat/eclipsesme-website-redesign`, commit `72986b916296e547df2ed1c92089dfa5c3b69616`, `assets/site.js` and `assets/consent.js`. EclipseIQ independently implements the same technical principles: explicit local simulation, production fail-closed, AJAX and provider-confirmed success, optional CAPTCHA, stored accept/reject preferences, delayed analytics loading and withdrawal. No stylesheet, visual template, form endpoint or analytics identifier reused. EclipseIQ has its own configuration and storage key.

## Form configuration
Edit `assets/config.js`:

- Default `mode: "development"` allows simulation only on `file:`, localhost, 127.0.0.1 and [::1]. `developmentResult: "success"` or `"error"` selects test feedback. Simulations never reset the form or claim delivery.
- Before launch set `mode: "production"` and the new EclipseIQ Formspree endpoint (`https://formspree.io/f/` plus your own form ID). Empty or invalid endpoints and unknown modes keep delivery disabled. The default development mode on a public hostname also keeps delivery disabled; it cannot simulate success there.
- Production uses HTTPS; local HTTP is allowed only for controlled production-mode tests. Production mode on `file:` cannot send. No URL parameter can enable simulation or change the endpoint.
- Success requires both a successful HTTP response and JSON `ok: true`. Network errors, malformed JSON, non-2xx, 429 and ambiguous responses preserve entries and never claim delivery. A 20-second timeout explains that a timed-out inquiry may have arrived. Duplicate sends are locked while pending and after confirmed success. Failed production attempts have a 10-second retry pause.
- HTML constraints, required text trimming, conditional phone/SMS validation and at least one contact preference, length limits and a honeypot provide accessible client controls. Enforce abuse controls in Formspree: client JavaScript cannot prevent direct endpoint abuse. Configure domain restrictions for `eclipseiq.ca` and any intended www domain, spam protection, recipient routing and a verified sender/recipient workflow in the provider dashboard.
- Do not put private recipient routing, provider API credentials or CAPTCHA secret keys in HTML/JS. The Formspree form ID and reCAPTCHA site key are public identifiers, not secrets.

## Optional reCAPTCHA v2
Set `recaptchaSiteKey` to the public v2 checkbox key and `requireRecaptcha: true` when the provider is configured to require it. Register permitted domains with Google and pair verification correctly in Formspree's supported setup. Missing required keys disable delivery; when a key is present, an unloaded, failed, expired or incomplete challenge blocks sending. CAPTCHA is never loaded in simulation mode. It is separate from optional analytics consent because it protects the requested form operation. Confirm the privacy notice and CSP allowlist before enabling. No key has been invented.

## Consent and GA4
- `eclipseiq.analytics-consent.v1` stores `accepted` or `rejected` with a timestamp for 180 days. Invalid, expired or future-dated entries do not grant consent. With blocked storage, choice is held for the page session only.
- The compact banner names no analytics vendor. Equal actions accept or reject; the footer reopens it, focuses the existing choice (reject by default), and returns focus after a decision. Escape closes it only after a choice exists. It is a non-modal region, so it does not trap keyboard focus.
- Analytics loads only after explicit acceptance, on hosted HTTPS, and only with a nonempty syntactically valid EclipseIQ `analytics.measurementId`. Local and file previews never collect. No noscript pixels, preconnects, third-party fonts or analytics tags appear in HTML.
- GA4 setup disables advertising signals, automatic initial page views and ad storage. A single explicit page view uses canonical URL/title and an empty referrer; it never deliberately reads input content, search strings or fragments. In GA4's data stream dashboard disable enhanced measurement (especially form interactions, outbound clicks and site search) to avoid remote settings collecting additional events. Code cannot control every future remote GA configuration.
- Rejecting disables GA immediately, clears the pending data layer, removes script elements, deletes accessible `_ga` cookies for site paths/domains where possible, then reloads if the provider was started. Reload unloads executing code. Third-party or HttpOnly cookies and previously collected data cannot be removed by this code.
- Cross-tab changes and clearing storage stop collection. Open tabs also check saved consent expiry every minute.
- The GA4 ID remains empty. No Statcounter integration or identifiers are included. Live GA4 behavior and actual Formspree delivery require post-configuration verification; browser tests mock both providers and send no real inquiries.
