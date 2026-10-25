"use strict";
// Public configuration only. Never put API secrets or private keys in this file.
window.ECLIPSEIQ_CONFIG = Object.freeze({
  form: Object.freeze({
    mode: "production", // Real delivery on HTTPS hosting; local previews simulate by default.
    allowLocalProduction: false, // Explicit opt-in ONLY for a deliberate local delivery test.
    developmentResult: "success", // "error" tests the accessible error path.
    endpoint: "https://formspree.io/f/mkjjoneb", // EclipseIQ inquiry endpoint (public).
    requireRecaptcha: true,
    recaptchaSiteKey: "6LcYYf8tAAAAAL1iEM5TbzaZSiq4VEGSsfyBUOna" // PUBLIC v2 checkbox key only.
  }),
  analytics: Object.freeze({
    measurementId: "G-2F668858GH",
    statcounter: Object.freeze({projectId: "13134286", securityCode: "a2936037", invisible: true})
  })
});
