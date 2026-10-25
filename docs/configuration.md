# Contact delivery, reCAPTCHA and analytics

## Current production configuration

`assets/config.js` contains only public settings:

- `mode: "production"`.
- Formspree endpoint: `https://formspree.io/f/mkjjoneb`.
- `requireRecaptcha: true`.
- Public reCAPTCHA v2 checkbox site key: `6LcYYf8tAAAAAL1iEM5TbzaZSiq4VEGSsfyBUOna`.
- `allowLocalProduction: false`.
- GA4 Measurement ID: `G-2F668858GH`.
- Invisible Statcounter project: `13134286`; public security code: `a2936037`.

The reCAPTCHA secret remains exclusively in Formspree. Never add a secret key, private recipient routing or provider API credential to this repository, browser code, URLs or test fixtures.

On HTTPS hosting, the contact form explicitly renders Google's v2 checkbox in the existing CAPTCHA container. Narrow forms use Google's supported compact widget. Missing, expired or unavailable verification blocks delivery. Expiry and load errors use the existing accessible status area. The token is sent under the required `g-recaptcha-response` field.

Inquiries are submitted asynchronously as `FormData` with `Accept: application/json`. Success requires **both** a successful HTTP status and JSON `ok: true`. The form never treats a click, a completed checkbox, a pending request, ambiguous JSON or a network timeout as confirmed receipt. Failures preserve entries; pending and confirmed submissions prevent duplicate sends. The existing 20-second timeout, retry pause, length/required-field validation, honeypot and email/phone/SMS preferences are preserved.

## Safe everyday local review

Open root `index.html` directly or run:

```sh
python -m http.server 4173
```

Then visit http://localhost:4173/contact/index.html.

Even though the committed mode is production, `file:`, localhost, 127.0.0.1 and [::1] default to **local simulation**. The existing notice and result explicitly say that no inquiry was sent. Google and Formspree are not contacted. `developmentResult` can select simulated success/error. No URL parameter can enable real delivery.

Public-host development mode still fails closed. Production on plain remote HTTP is disabled. A file-origin page cannot send a production inquiry, even if local production is explicitly enabled.

## Deliberate real submission test locally

This is a manual end-to-end test that sends one real inquiry. Automated browser checks use intercepted providers and never send real inquiries.

1. In the Google reCAPTCHA admin console, ensure the supplied **checkbox** key permits the hostname you will use, such as `localhost`. For production, ensure `eclipseiq.ca` and any intended `www` hostname are permitted. Keep server-side validation enabled. The existing secret stays in Formspree.
2. In Formspree, confirm the dedicated form, custom reCAPTCHA configuration, recipient routing and any domain restrictions permit the intended test. If localhost is restricted, use a permitted staging hostname or temporarily allow the local test through the provider settings; do not disable CAPTCHA validation. Restore temporary provider allowances after testing.
3. From the repository root, explicitly start the opt-in loopback preview:

   ```sh
   python scripts/preview_form_delivery.py --real-delivery --port 4174
   ```

   Open http://localhost:4174/contact/index.html (or 127.0.0.1 if that hostname is allowed for the key). The helper serves an **in-memory** configuration with local production enabled, binds only to loopback, and does not edit repository files. Starting an ordinary static server does not opt in.
4. Confirm the page shows the normal secure-inquiry notice and the real Google checkbox, rather than the local-simulation notice. Fill every required field with clearly labelled test information and an email inbox you control. For Phone/SMS, include a test contact number you control. Do not include real policyholder or confidential data.
5. Before checking CAPTCHA, submit once: verification should block sending. Complete the actual Google challenge, then submit once. In browser developer tools, confirm one POST to the configured endpoint, including `g-recaptcha-response`. Do not copy or publish the token.
6. Confirm success appears only after Formspree responds successfully. Check the Formspree submissions dashboard and intended recipient inbox for the labelled test. HTTP acceptance confirms Formspree receipt; checking the inbox verifies downstream mail delivery.
7. Stop the preview with Ctrl+C. Returning to the ordinary local server restores simulation automatically. No tracked configuration needs reverting. Do not commit `allowLocalProduction: true`.

If Google displays “invalid domain for site key” or cannot load, no real inquiry can be sent. Correct the provider-side hostname/setup or network issue and retry; the client cannot verify provider dashboard configuration by itself.

## Automated checks

Start the ordinary local server and run `python scripts/check_browser.py`. It tests validation, preferences, spam guards, CAPTCHA rendering/token handling/expiry/errors, normal/compact widget sizing, pending requests, duplicate prevention, token POST payloads, provider-confirmed success and failure, safe local defaults and deliberate local opt-in using mocked providers. All production-like Google/Formspree traffic is intercepted.

The live key's domain permissions, private Formspree setup and actual mailbox delivery require the manual test above; they are not established by mocked tests.

## Consent and analytics

Both services are configured in `assets/config.js` and run only on public HTTPS pages after explicit acceptance, or a valid previously accepted preference (180 days). The consent storage version is now `eclipseiq.analytics-consent.v2`: preferences from the earlier GA-only preparation prompt for a new choice before enabling either provider. No provider script, analytics request, preconnect or noscript tracking image is present before consent. File and loopback previews never collect analytics, even after acceptance or when the form delivery helper is used. CAPTCHA protects the requested form operation and is separate from optional usage analytics.

GA4 loads its tag once per document, configures `send_page_view: false`, then queues exactly one explicit `page_view`. Its location is the static canonical URL, its title is the fixed document title, and its referrer is empty. Advertising signals and personalization are disabled. There are no custom form, conversion, user-ID or contact-detail events. **In the GA4 web stream dashboard, keep Enhanced Measurement disabled** (including history page views, form interactions, site search and outbound clicks), and do not add automatic user-provided data collection or additional tags. Those remotely managed settings cannot be verified from this repository. Review property retention and access before launch.

Statcounter uses its invisible counter image transport (`https://c.statcounter.com/t.php`) with the supplied project/security code and `invisible=1`. Only the canonical page URL (`u`), fixed title (`t`), blank referrer (`camefrom`) counter configuration and a cache-busting timestamp are supplied. `referrerPolicy="no-referrer"` also prevents the browser from attaching the current address. We deliberately omit `counter.js`, replay, click tracking, visitor labels and the noscript pixel. This limits Statcounter to page-view statistics; advanced visitor/session reports may be limited. The image request still exposes normal network metadata to the provider. This implementation creates no Statcounter visitor cookie.

Reopening preferences and accepting again does not duplicate initialization. Withdrawal removes analytics elements and accessible GA/legacy Statcounter cookies, disables GA, and reloads to unload executing provider code. Saved rejection, expiry, invalid preferences and cross-tab withdrawal fail closed. Third-party/HttpOnly cookies and already received data cannot be removed by website JavaScript.

### Analytics verification

Run `python scripts/check_browser.py` with the ordinary local server running. Provider requests are intercepted: no test visits or real inquiries reach Google, Statcounter or Formspree. The suite covers fresh visitors, persistent rejection, accepted returning visitors, repeat acceptance, withdrawal, expired/invalid choices, cross-tab changes, blocked storage, disabled JavaScript, sanitized payloads and untouched local simulation.

On a separately authorized HTTPS staging/production host, use Developer Tools Network with Preserve log enabled. Clear site data and verify no Google Analytics/Tag Manager/Statcounter request before choosing; Reject and reload should remain silent. Accept should load one GA tag and one invisible Statcounter request with the canonical URL and no query values or referrer. Check GA4 network `page_view` count/Realtime and Statcounter reports; reload should register one new page view per provider without reopening the banner. Reaccepting on the same page should register none. Withdraw through Cookie preferences, check accessible cookies are removed, and reload/navigate: no new tracking. Test a URL containing a non-personal test query and confirm its value never appears in provider requests. No live provider reporting or dashboard configuration is established by intercepted tests.

Implementation references: [Formspree custom reCAPTCHA v2](https://help.formspree.io/articles/form-and-project-settings/adding-a-custom-recaptcha-v2-key/) and [Google's explicit checkbox rendering API](https://developers.google.com/recaptcha/docs/display).
