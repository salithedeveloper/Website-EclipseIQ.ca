# Contact delivery, reCAPTCHA and analytics

## Production configuration

`assets/config.js` contains only public settings:

- `mode: "production"`.
- Formspree endpoint: `https://formspree.io/f/mkjjoneb`.
- `requireRecaptcha: true`.
- Public reCAPTCHA v2 checkbox site key: `6LcYYf8tAAAAAL1iEM5TbzaZSiq4VEGSsfyBUOna`.
- GA4 Measurement ID: `G-2F668858GH`.
- Invisible Statcounter project: `13134286`; public security code: `a2936037`.

The reCAPTCHA secret remains exclusively in Formspree. Never add a secret key, private recipient routing or provider API credential to this repository, browser code, URLs or test fixtures.

The form sends real inquiries on HTTPS hosting and on HTTP localhost, 127.0.0.1 and [::1]. There is no simulation mode or local delivery override. Plain HTTP on other hosts and direct `file:` previews cannot submit. Direct file previews explain that a local web server is required.

Google's v2 checkbox renders in the existing CAPTCHA container, using compact sizing on narrow forms. Missing, expired or unavailable verification blocks delivery. The token is sent as `g-recaptcha-response`. Inquiries are submitted asynchronously as `FormData` with `Accept: application/json`. Success requires **both** a successful HTTP status and JSON `ok: true`. A click, checked CAPTCHA, pending request, ambiguous JSON or timeout never counts as confirmed receipt. Failures preserve entries; pending and confirmed submissions prevent duplicates. The 20-second timeout, retry pause, required-field/length validation, honeypot and email/phone/SMS preferences remain intact.

## Local review and real submission test

Ordinary local submissions now send real inquiries after CAPTCHA; no special helper or configuration change is needed. Automated tests intercept all provider traffic and do not send inquiries.

1. In Google's reCAPTCHA admin console, ensure the checkbox key permits the hostname used for testing, such as `localhost`. Ensure production hostnames are permitted as well. Keep server-side verification enabled and the private secret in Formspree. Confirm Formspree recipient routing and domain restrictions permit the test origin.
2. From the repository root run:

   ```sh
   python -m http.server 4173 --bind 127.0.0.1
   ```

   Open http://localhost:4173/contact/index.html. Opening the HTML directly cannot deliver inquiries. The obsolete opt-in preview helper has been removed.
3. Confirm the real checkbox appears. Fill required fields with clearly labelled test information and an inbox you control. Do not include confidential or policyholder information. Phone/SMS preferences require a phone number.
4. Submit before checking CAPTCHA: delivery must be blocked. Complete the actual Google challenge and submit once. In browser Network tools, confirm one POST to the configured endpoint with `g-recaptcha-response`. Do not publish the token.
5. Confirm success appears only after Formspree responds successfully. Verify the submission in Formspree and the intended recipient inbox; provider HTTP acceptance does not establish downstream email delivery.
6. Stop the server with Ctrl+C. No configuration needs reverting. Local analytics remains disabled.

If Google reports an invalid domain or fails to load, sending stays blocked. Correct provider-side hostname/settings or network access rather than bypassing CAPTCHA. Provider dashboard configuration and mailbox delivery require this manual end-to-end check.

## Automated checks

Start the local server, then run `python scripts/check_browser.py`. Browser routes intercept Google, Formspree and analytics requests. The suite verifies hosted and all three loopback origins, required fields, contact preferences, honeypot, CAPTCHA rendering/expiry/errors/token handling, provider-confirmed success, malformed/rejected/network responses, pending and duplicate protection, and disabled non-loopback HTTP. No real inquiry is sent by these tests.

## Consent and analytics

Both services are configured in `assets/config.js` and run only on public HTTPS pages after explicit acceptance, or a valid previously accepted preference (180 days). The consent storage version is now `eclipseiq.analytics-consent.v2`: preferences from the earlier GA-only preparation prompt for a new choice before enabling either provider. No provider script, analytics request, preconnect or noscript tracking image is present before consent. File and loopback previews never collect analytics, even after acceptance. CAPTCHA protects the requested form operation and is separate from optional usage analytics.

GA4 loads its tag once per document, configures `send_page_view: false`, then queues exactly one explicit `page_view`. Its location is the static canonical URL, its title is the fixed document title, and its referrer is empty. Advertising signals and personalization are disabled. There are no custom form, conversion, user-ID or contact-detail events. **In the GA4 web stream dashboard, keep Enhanced Measurement disabled** (including history page views, form interactions, site search and outbound clicks), and do not add automatic user-provided data collection or additional tags. Those remotely managed settings cannot be verified from this repository. Review property retention and access before launch.

Statcounter uses its invisible counter image transport (`https://c.statcounter.com/t.php`) with the supplied project/security code and `invisible=1`. Only the canonical page URL (`u`), fixed title (`t`), blank referrer (`camefrom`) counter configuration and a cache-busting timestamp are supplied. `referrerPolicy="no-referrer"` also prevents the browser from attaching the current address. We deliberately omit `counter.js`, replay, click tracking, visitor labels and the noscript pixel. This limits Statcounter to page-view statistics; advanced visitor/session reports may be limited. The image request still exposes normal network metadata to the provider. This implementation creates no Statcounter visitor cookie.

Reopening preferences and accepting again does not duplicate initialization. Withdrawal removes analytics elements and accessible GA/legacy Statcounter cookies, disables GA, and reloads to unload executing provider code. Saved rejection, expiry, invalid preferences and cross-tab withdrawal fail closed. Third-party/HttpOnly cookies and already received data cannot be removed by website JavaScript.

### Analytics verification

Run `python scripts/check_browser.py` with the ordinary local server running. Provider requests are intercepted: no test visits or real inquiries reach Google, Statcounter or Formspree. The suite covers fresh visitors, persistent rejection, accepted returning visitors, repeat acceptance, withdrawal, expired/invalid choices, cross-tab changes, blocked storage, disabled JavaScript, sanitized payloads and local contact delivery with intercepted providers.

On a separately authorized HTTPS staging/production host, use Developer Tools Network with Preserve log enabled. Clear site data and verify no Google Analytics/Tag Manager/Statcounter request before choosing; Reject and reload should remain silent. Accept should load one GA tag and one invisible Statcounter request with the canonical URL and no query values or referrer. Check GA4 network `page_view` count/Realtime and Statcounter reports; reload should register one new page view per provider without reopening the banner. Reaccepting on the same page should register none. Withdraw through Cookie preferences, check accessible cookies are removed, and reload/navigate: no new tracking. Test a URL containing a non-personal test query and confirm its value never appears in provider requests. No live provider reporting or dashboard configuration is established by intercepted tests.

Implementation references: [Formspree custom reCAPTCHA v2](https://help.formspree.io/articles/form-and-project-settings/adding-a-custom-recaptcha-v2-key/) and [Google's explicit checkbox rendering API](https://developers.google.com/recaptcha/docs/display).
