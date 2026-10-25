# Contact delivery, reCAPTCHA and analytics

## Current production configuration

`assets/config.js` contains only public settings:

- `mode: "production"`.
- Formspree endpoint: `https://formspree.io/f/mkjjoneb`.
- `requireRecaptcha: true`.
- Public reCAPTCHA v2 checkbox site key: `6LcYYf8tAAAAAL1iEM5TbzaZSiq4VEGSsfyBUOna`.
- `allowLocalProduction: false`.
- Analytics Measurement ID remains empty; analytics code and consent behaviour are unchanged.

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

The existing consent controls and analytics preparation remain unchanged. The GA4 ID stays empty. Local/file previews never collect analytics; public analytics requires a configured ID and explicit consent. Rejection, withdrawal, expiry and cross-tab synchronization retain their existing behaviour. CAPTCHA protects the requested form operation and is not optional website-usage analytics.

Implementation references: [Formspree custom reCAPTCHA v2](https://help.formspree.io/articles/form-and-project-settings/adding-a-custom-recaptcha-v2-key/) and [Google's explicit checkbox rendering API](https://developers.google.com/recaptcha/docs/display).
