# Live website audit and redesign comparison

This audit supersedes the cached-only findings in the first iteration. Live HTTP access succeeded on retry. Audited 23 October 2026 (Toronto client date).

## Access and crawl evidence

| Request | Result |
| --- | --- |
| `https://eclipseiq.ca/` | HTTP 200, 98,217 bytes of HTML |
| `https://www.eclipseiq.ca/` | HTTP 200 after redirect to apex, same 98,217-byte homepage |
| `/contact/` | HTTP 200, 190,762 bytes |
| `/faq/` | HTTP 200, 134,394 bytes |
| `/privacy-policy/` | HTTP 200, 116,354 bytes |
| `/cookie-policy-ca/` | HTTP 200, 117,724 bytes; empty article with consent UI |
| `/cookie-policy-ca-2/` | HTTP 200, 120,529 bytes; generated Canadian cookie policy |
| `/about/`, `/services/` | HTTP 404: not separate public pages on the live site |
| `/robots.txt` | HTTP 200 |
| `/wp-sitemap.xml`, `/sitemap_index.xml` | HTTP 200; both identify `/page-sitemap.xml` |
| `/page-sitemap.xml` | HTTP 200; six public page URLs, all fetched |
| `/wp-json/wp/v2/pages?per_page=100` | HTTP 200; six published pages, matching the sitemap |

Read every same-domain public link found on fetched pages. Services and About are sections on the homepage, not standalone source pages. Privacy/cookie content was discoverable through the sitemap/API even though the extracted footer did not expose useful links. The published page inventory was reconciled against both sitemap and REST page list. External LinkedIn and EclipseSME links were inventoried without making changes to either service. No forms submitted, authentication/private admin paths accessed, or WordPress settings changed.

## Actual branding and asset provenance

Original logo (retrieved byte-for-byte, not recreated):
`https://eclipseiq.ca/wp-content/uploads/2025/04/EclipseIQ-Logo-202-x-88-px.png`

WordPress media endpoint `wp-json/wp/v2/media?search=EclipseIQ&per_page=100` identifies media 183 and the original 202×88 PNG as the full-size asset. Its aspect ratio, pixels, wording and white background are preserved. No larger source was exposed. Display at intrinsic dimensions or smaller; do not trace, recolour, invert or upscale as a new logo.

Verified source colours from the homepage inline Divi styles:
- `#023047`: deep blue, links, CTA surfaces and final section.
- `#219ebc`: turquoise, service icons, CTA buttons and highlighted column.
- `#FFFFFF`, `#111111`: primary surfaces/text.
- `#7EBEC5`: secondary legacy accent.
- Original logo pixel analysis: dominant saturated blue `#13A8FF` (19,168,255), plus black, white and grey.

Typography: source explicitly declares IBM Plex Sans and IBM Plex Sans Condensed. The revision self-hosts Latin WOFF2 versions of these families with their SIL Open Font License. No runtime third-party font requests.

Original photos/graphics retrieved for inspection:
- `/wp-content/uploads/2024/09/EIS_BrainStorming.png` (800×534): business discussion photograph. Reused as existing-site editorial imagery; not represented as the EclipseIQ team or office.
- `/wp-content/uploads/2024/09/EclipseSME_LandingPage.png` (1872×955): historical product marketing screenshot with example metrics. Not reused as current product UI or evidence of real customer performance.

## Content inventory and treatment

| Source content | Substance | Revised treatment |
| --- | --- | --- |
| Homepage lead | Modernize technology and operations for insurers, MGAs, reinsurers and brokers | Explicit audience and insurance technology positioning above the fold |
| Insurance Solutions | Tailored software, including EclipseSME | Dedicated product section alongside services |
| Professional Services | Insurance operational expertise | Visible advisory, implementation and leadership paths |
| Support and Service | Guidance and support | Retained in service overview and contact paths; no invented SLA or 24/7 promise |
| Insurance SaaS | EclipseSME implementation and policy administration | Dedicated software offering and product lifecycle explanation |
| Strategic Consulting | Business/operations strategy | Named offering, not generic strategy copy |
| Digital Transformation and Technology Integration | Underwriting, policy and claims workflows; integration | Named offering with architecture, modernization and integration detail |
| Team Development and Coaching | Leadership, team efficiency, operational performance | Named offering with substantive copy |
| Fractional CIO / COO / CTO Leadership | Interim executive guidance through transition or complex projects | All three titles retained and distinguished without invented biographies |
| Totality Check / Eclipse Totality Assessment™ | Business, systems, process, data, integration and governance review; prioritized roadmap | FAQ's fuller assessment name used consistently; original “Totality Check” noted |
| Audit Readiness | Compliance/documentation/process review | Standalone named service; no guaranteed compliance or certification |
| Security Review | Systems vulnerability/cybersecurity review | Standalone named service; no invented accreditation |
| Product benefits | Policy management, workflow automation, reporting | Three distinct benefits; product external links and demonstration CTA |
| About section | Canadian base, decades of executive and hands-on insurance experience, architecture, modernization, data/analytics, reinsurance and enterprise transformation | Explicit corporate narrative and expertise coverage |
| FAQ | Services, demo, pricing, international work, product, timelines, custom solutions, third-party platforms, migration, transformation approach, assessment, audiences, fractional leadership, legacy modernization | All 14 question topics retained; timelines qualified as scoped and variable |
| Contact | Name, email, company/type, email/phone/SMS preferences, service interests, comments | Original information needs restored in accessible form; no live endpoint invented |
| Privacy | Contact/technical data, purposes, no sale/rental, processors/legal sharing, safeguards, access/correction/deletion and marketing choice | Scoped modern website notice retains relevant principles and explains actual static-site controls; unverified compliance guarantees excluded |
| Cookie policies | Generated cookie explanations; duplicates, stale WordPress/shopping/marketing references | Concise current controls at privacy-policy page; preserve old URLs through local compatibility pages and documented launch redirects |

## What the first redesign missed

1. The actual logo was missing. The approximation of brand colours and generic serif typography broke continuity with the existing brand.
2. The opening “Built on insurance” slogan was less explicit than the source about modernization, insurance audiences and concrete services.
3. Eight named offerings were collapsed into five broad categories. Team development, audit readiness and security review lost prominence; COO/CTO leadership was narrowed to technology leadership.
4. Source software benefits, claims workflow context, reinsurance and data/analytics expertise were underrepresented.
5. The design used a long repeated ruled-list structure and generic orbit illustration. These gave it a consultancy-template feel instead of a distinct EclipseIQ presentation.
6. The original contact preference for SMS was omitted and company/service context was simplified too far.
7. Only cached navigation was inventoried. The three real privacy/cookie URLs were missed, so the original URL preservation guidance was incomplete.
8. Original fonts and existing-site imagery were unavailable and replaced without enough continuity. The revision uses the verified fonts and an existing image deliberately, without claiming it depicts company employees.

## Revision direction

A substantial composition change: white brand header with actual logo; large condensed typography; bright blue/turquoise colour blocks and deep blue corporate surfaces; insurance-specific editorial hero; clear three-part overview (software, advisory, leadership); all eight named offerings with dedicated detail; richer company expertise and a discrete EclipseSME feature. Retain existing service language while rewriting for clarity. Replace the orbit diagram and repetitive service list. No copy, CSS or visual design imported from EclipseSME; existing form/consent implementations remain technically grounded in the previously reviewed reference.

## Remaining verification limits
No live Formspree endpoint, reCAPTCHA key or GA4 property ID supplied. The site must remain safe without them. Public company claims are grounded in the live first-party pages; no external certifications, named clients, partnerships, staff identities, or statistics invented. Street address and private routing are not published. Existing policy wording still requires owner review for current business practices and retention handling before launch. Nothing is deployed.
