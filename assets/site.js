"use strict";
(() => {
  document.documentElement.classList.add("js");
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.getElementById("navigation");
  const closeMenu = () => {
    toggle?.setAttribute("aria-expanded", "false");
    nav?.classList.remove("is-open");
  };
  if (toggle && nav) {
    toggle.hidden = false;
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") !== "true";
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
    });
    document.addEventListener("keydown", e => {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        closeMenu(); toggle.focus();
      }
    });
    document.addEventListener("click", e => { if (!e.target.closest(".header")) closeMenu(); });
    nav.addEventListener("click", e => { if (e.target.closest("a")) closeMenu(); });
    window.matchMedia("(min-width: 851px)").addEventListener("change", closeMenu);
  }

  const form = document.getElementById("inquiry-form");
  if (!form) return;
  const config = window.ECLIPSEIQ_CONFIG?.form || {};
  const local = ["localhost", "127.0.0.1", "[::1]"].includes(location.hostname);
  const production = config.mode === "production";
  const validEndpoint = typeof config.endpoint === "string" && /^https:\/\/formspree\.io\/f\/[a-zA-Z0-9]+$/.test(config.endpoint);
  const secureTransport = location.protocol === "https:" || (local && location.protocol === "http:");
  const publicKey = typeof config.recaptchaSiteKey === "string" ? config.recaptchaSiteKey.trim() : "";
  const ready = production && validEndpoint && secureTransport && (!config.requireRecaptcha || publicKey);
  const submit = form.querySelector('[type="submit"]');
  const status = document.getElementById("form-status");
  const note = document.getElementById("delivery-note");
  const phone = document.getElementById("phone");
  let pending = false, received = false, retryAfter = 0, captchaWidget;
  function message(text, state = "error", focus = false) {
    status.hidden = false; status.dataset.state = state; status.textContent = text;
    if (focus) status.focus();
  }
  submit.disabled = !ready;
  note.textContent = ready ? "Send your inquiry securely. Please do not include confidential or policyholder information."
    : location.protocol === "file:" ? "To send an inquiry, open this site through a localhost web server or HTTPS hosting."
    : "Online inquiries are currently unavailable. No inquiry will be sent until the contact service is configured.";
  if (!ready) message(location.protocol === "file:" ? "Direct file previews cannot send inquiries. Please use a localhost web server." : "The contact service is not configured for live delivery. Please try again later.");
  const interest = new URLSearchParams(location.search).get("interest");
  const select = document.getElementById("interest");
  if (interest && [...select.options].some(o => o.value === interest)) select.value = interest;
  if (ready && production && publicKey) {
    window.eclipseIQCaptchaReady = () => {
      try {
        captchaWidget = window.grecaptcha.render("form-captcha", {
          sitekey: publicKey,
          size: document.getElementById("form-captcha").clientWidth < 304 ? "compact" : "normal",
          "expired-callback": () => { if (!received && !pending) message("Spam verification expired. Please complete the checkbox again."); },
          "error-callback": () => { if (!received && !pending) message("Spam verification could not complete. Please refresh and try again."); }
        });
      } catch {
        message("Spam verification could not load. Please refresh and try again.");
      }
    };
    const script = document.createElement("script");
    script.src = "https://www.google.com/recaptcha/api.js?onload=eclipseIQCaptchaReady&render=explicit";
    script.async = true;
    script.onerror = () => message("Spam verification could not load. Please refresh and try again.");
    document.head.append(script);
  }
  const clearPhoneError = () => phone.setCustomValidity("");
  phone.addEventListener("input", clearPhoneError);
  form.querySelectorAll('[name="contact_method"]').forEach(n => n.addEventListener("change", clearPhoneError));
  form.addEventListener("submit", async event => {
    event.preventDefault();
    if (!ready || pending || received) return;
    if (Date.now() < retryAfter) { message("Please wait a few seconds before retrying. Your entries are preserved.", "error", true); return; }
    for (const id of ["name", "email", "company", "message"]) document.getElementById(id).value = document.getElementById(id).value.trim();
    clearPhoneError();
    const methods = new FormData(form).getAll("contact_method");
    if ((methods.includes("Phone") || methods.includes("SMS")) && !phone.value.trim()) phone.setCustomValidity("Please provide a phone number for a call or text.");
    if (!methods.length) { message("Please select at least one preferred contact method.", "error", true); form.querySelector('[name="contact_method"]').focus(); return; }
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    if (data.get("_gotcha")) { message("Unable to submit this inquiry. Please try again later.", "error", true); return; }
    if (production && publicKey) {
      let token = "";
      try { if (captchaWidget !== undefined) token = window.grecaptcha?.getResponse(captchaWidget) || ""; } catch { /* Block delivery if verification is unavailable. */ }
      if (!token) { message("Please complete the spam verification before sending.", "error", true); return; }
      data.set("g-recaptcha-response", token);
    }
    pending = true; submit.disabled = true; submit.textContent = "Sending…";
    form.setAttribute("aria-busy", "true");
    message("Sending your inquiry…", "pending");
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 20000);
    try {
      const response = await fetch(config.endpoint, {method:"POST", body:data, headers:{Accept:"application/json"}, credentials:"omit", referrerPolicy:"strict-origin-when-cross-origin", signal:controller.signal});
      const result = await response.json();
      if (!response.ok || result?.ok !== true) throw new Error("provider");
      received = true;
      form.reset();
      message("Thank you. Your inquiry has been received. We’ll be in touch to discuss your priorities.", "success", true);
    } catch {
      retryAfter = Date.now() + 10000;
      message("We could not confirm receipt. Your entries are preserved. Please wait a few seconds and try again. If the connection timed out, your inquiry may already have arrived.", "error", true);
    } finally {
      clearTimeout(timer); pending = false; form.removeAttribute("aria-busy");
      submit.disabled = received; submit.textContent = received ? "Inquiry received" : "Send inquiry";
      if (production && !received && captchaWidget !== undefined) {
        try { window.grecaptcha?.reset(captchaWidget); } catch { /* The next attempt still requires a valid token. */ }
      }
    }
  });
})();
