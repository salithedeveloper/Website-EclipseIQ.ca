# URL continuity

Known source pages from the recovered public navigation:

| Existing URL | Redesign | Action |
| --- | --- | --- |
| `/` | `/index.html` served at `/` | Preserve |
| `/contact/` | `/contact/index.html` | Preserve directory index |
| `/faq/` | `/faq/index.html` | Preserve directory index |
| Homepage offerings/about/product sections | `/#capabilities`, `/about/`, `/#eclipsesme` | New explicit destinations |

New pages: `/services/`, `/about/`, `/privacy/`. The old footer's Privacy Policy was plain text in extracted content, so no verified historical privacy URL is known. Do not fabricate an old URL or create broad redirects. All internal links include explicit index filenames for File Explorer support; canonicals and sitemap use conventional directory URLs.

Before WordPress replacement export all published URLs and consult Search Console/Hostinger logs. Add specific 301 redirects for real legacy URLs and old anchor destinations once known. A server cannot redirect fragments; retain any important old anchor IDs after obtaining an export. Preserve uploaded assets that have inbound links where required. Keep `/wp-admin/` and other WordPress paths out of the static deployment; do not indiscriminately redirect them to the homepage.

For Apache/Hostinger, configure directory indexes and the 404 document only after review:

```
DirectoryIndex index.html
ErrorDocument 404 /404.html
```

These lines are documentation, not a deployed `.htaccess`. No server behavior has been changed.
