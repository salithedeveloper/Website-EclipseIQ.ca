"use strict";
(() => {
  const banner = document.getElementById("cookie-banner");
  const preferences = document.querySelector(".cookie-preferences");
  if (!banner || !preferences) return;
  const key = "eclipseiq.analytics-consent.v2";
  const maxAge = 180 * 24 * 60 * 60 * 1000;
  const analytics = window.ECLIPSEIQ_CONFIG?.analytics || {};
  const id = analytics.measurementId || "";
  const counter = analytics.statcounter || {};
  const validCounter = /^\d+$/.test(counter.projectId || "") && /^[a-f0-9]{8}$/i.test(counter.securityCode || "") && counter.invisible === true;
  // Preview and file origins never collect analytics, including when production IDs are configured.
  const hosted = location.protocol === "https:" && !["localhost", "127.0.0.1", "[::1]"].includes(location.hostname);
  const validId = /^G-[A-Z0-9]+$/.test(id);
  let choice = null, started = false, returnFocus;
  const valid = s => s && ["accepted", "rejected"].includes(s.choice) && Number.isFinite(s.at) && s.at <= Date.now() && Date.now() - s.at < maxAge;
  try { const saved = JSON.parse(localStorage.getItem(key)); if (valid(saved)) choice = saved.choice; } catch { /* Fail closed if storage is unavailable. */ }
  function clearCookies() {
    try {
      const names = document.cookie.split(";").map(c => c.trim().split("=")[0]).filter(n => /^(?:_ga(?:_|$)|sc_is_visitor_unique$|is_unique$|is_visitor_unique$)/.test(n));
      const domains = ["", location.hostname, "." + location.hostname];
      if (location.hostname.endsWith(".eclipseiq.ca")) domains.push("eclipseiq.ca", ".eclipseiq.ca");
      const parts = location.pathname.split("/");
      const paths = new Set(["/"]);
      for (let i = 1; i < parts.length; i++) paths.add(parts.slice(0, i).join("/") + "/");
      for (const name of names) for (const domain of domains) for (const path of paths) document.cookie = `${name}=; Max-Age=0; path=${path}${domain ? "; domain=" + domain : ""}; SameSite=Lax`;
    } catch { /* Some origins restrict cookies. Third-party and HttpOnly cookies are inaccessible. */ }
  }
  function start() {
    if (choice !== "accepted" || started || !hosted || (!validId && !validCounter)) return;
    // Only a trusted, static canonical URL may enter analytics. Never use location.href,
    // document.referrer, form values, custom user IDs or campaign query parameters.
    let canonical;
    try {
      canonical = new URL(document.querySelector('link[rel="canonical"]')?.href);
      if (canonical.origin !== "https://eclipseiq.ca" || canonical.search || canonical.hash) return;
    } catch { return; }
    canonical = canonical.href;
    started = true;
    if (validId) {
      window["ga-disable-" + id] = false;
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag("consent", "default", {analytics_storage:"granted",ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied"});
      window.gtag("js", new Date());
      const page = {page_location:canonical,page_title:document.title,page_referrer:""};
      window.gtag("set", page);
      window.gtag("config", id, {...page,send_page_view:false,allow_google_signals:false,allow_ad_personalization_signals:false});
      window.gtag("event", "page_view", {...page,send_to:id});
      const script = document.createElement("script");
      script.dataset.optionalAnalytics = "ga4";
      script.src = "https://www.googletagmanager.com/gtag/js?id=" + id;
      script.async = true; script.referrerPolicy = "no-referrer";
      document.head.append(script);
    }
    if (validCounter) {
      // Page-view-only invisible image transport. Do not load counter.js: its
      // automatic URL/referrer, click and replay collection exceeds our scope.
      // These are the counter protocol's page URL/title fields, not visitor input.
      const url = new URL("https://c.statcounter.com/t.php");
      url.search = new URLSearchParams({sc_project:counter.projectId,security:counter.securityCode,
        invisible:"1",java:"1",u:canonical,t:document.title,camefrom:"",r:String(Date.now())}).toString();
      const pixel = document.createElement("img");
      pixel.dataset.optionalAnalytics = "statcounter";
      pixel.alt = ""; pixel.width = 1; pixel.height = 1; pixel.hidden = true;
      pixel.referrerPolicy = "no-referrer";
      pixel.src = url.href;
      document.body.append(pixel);
    }
  }
  function stop() {
    if (validId) window["ga-disable-" + id] = true;
    if (window.dataLayer) window.dataLayer.length = 0;
    document.querySelectorAll("[data-optional-analytics]").forEach(n => n.remove());
    clearCookies();
    if (started) location.reload(); // Unload already executing provider code.
  }
  function close() { banner.hidden = true; if (returnFocus?.isConnected) returnFocus.focus(); }
  function apply(next, persist = true) {
    choice = next;
    if (persist) {
      try {
        if (next === "rejected") localStorage.removeItem(key);
        localStorage.setItem(key, JSON.stringify({choice,at:Date.now()}));
      } catch { /* Current-page explicit choice remains effective. */ }
    }
    close();
    if (next === "accepted") start(); else stop();
  }
  preferences.hidden = false;
  preferences.addEventListener("click", () => {
    returnFocus = preferences; banner.hidden = false;
    banner.querySelector(`[data-cookie-choice="${choice || "rejected"}"]`).focus();
  });
  banner.querySelectorAll("[data-cookie-choice]").forEach(b => b.addEventListener("click", () => apply(b.dataset.cookieChoice)));
  banner.addEventListener("keydown", e => { if (e.key === "Escape" && choice) { e.preventDefault(); close(); } });
  window.addEventListener("storage", e => {
    if (e.key !== key && e.key !== null) return;
    let saved; try { saved = e.key === null ? null : JSON.parse(e.newValue); } catch { /* Invalid state means no consent. */ }
    if (valid(saved)) apply(saved.choice, false);
    else { choice = null; stop(); banner.hidden = false; }
  });
  // An open tab also stops when a saved preference expires.
  setInterval(() => {
    if (!choice) return;
    try {
      const saved = JSON.parse(localStorage.getItem(key));
      if (!valid(saved)) { choice = null; stop(); banner.hidden = false; }
    } catch { /* Storage unavailable: keep current-page choice only. */ }
  }, 60000);
  if (choice === "accepted") start();
  else { clearCookies(); banner.hidden = choice === "rejected"; }
})();
