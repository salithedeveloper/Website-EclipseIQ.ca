"use strict";
// Public configuration only. Never put API secrets or private keys in this file.
window.ECLIPSEIQ_CONFIG = Object.freeze({
  form: Object.freeze({
    mode: "development", // Simulates ONLY on file:, localhost, 127.0.0.1 or [::1].
    developmentResult: "success", // "error" tests the accessible error path.
    endpoint: "", // Supply EclipseIQ's own https://formspree.io/f/FORM_ID.
    requireRecaptcha: false,
    recaptchaSiteKey: "" // Optional PUBLIC reCAPTCHA v2 site key; never a secret key.
  }),
  analytics: Object.freeze({measurementId: ""}) // EclipseIQ's own GA4 ID later.
});
