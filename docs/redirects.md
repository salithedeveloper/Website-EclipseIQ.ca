# Verified URL continuity

Live sitemap and WordPress public pages API expose six published URLs, all audited successfully.

| Existing URL | Static result | Launch action |
| --- | --- | --- |
| `/` | `/index.html` served at `/` | Preserve |
| `/contact/` | `/contact/index.html` | Preserve |
| `/faq/` | `/faq/index.html` | Preserve |
| `/privacy-policy/` | `/privacy-policy/index.html` | Preserve with updated website privacy/cookie notice |
| `/cookie-policy-ca/` | Working compatibility index, canonical privacy-policy | Prefer a specific 301 to `/privacy-policy/#cookies` when hosting is configured |
| `/cookie-policy-ca-2/` | Working compatibility index, canonical privacy-policy | Prefer a specific 301 to `/privacy-policy/#cookies` when hosting is configured |
| `/#offerings-section` | Same anchor retained on homepage | Preserve; `#capabilities` also works from the first redesign |

`/about/` and `/services/` return 404 on the original WordPress site: these are new information-architecture pages, not discovered legacy URLs. `/privacy/` was introduced by the first redesign; it remains a functional compatibility page with canonical `/privacy-policy/`. Duplicate compatibility pages use noindex and are omitted from the sitemap; no JavaScript redirect interferes with direct file browsing.

`https://www.eclipseiq.ca/` currently redirects to the apex domain. Preserve that host preference and HTTPS during any future hosting change. Canonicals use the apex. All internal file paths include `index.html` so File Explorer browsing works; directory URL canonicals remain appropriate for conventional hosting.

Before replacing WordPress, confirm any older/non-published URLs in Search Console and server logs. The current published sitemap/API inventory is verified, but it cannot prove the absence of historical deleted URLs or external backlinks. Preserve uploaded asset paths if inbound links require them. No blanket redirect to homepage.

Optional Apache/Hostinger configuration after separate launch approval:

```
DirectoryIndex index.html
ErrorDocument 404 /404.html
Redirect 301 /cookie-policy-ca/ https://eclipseiq.ca/privacy-policy/#cookies
Redirect 301 /cookie-policy-ca-2/ https://eclipseiq.ca/privacy-policy/#cookies
```

These are review examples only. Verify syntax/order with the hosting setup before use; no `.htaccess` or live server settings have been modified.
