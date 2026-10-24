# Asset provenance and branding

## Corporate logo

`assets/eclipseiq-logo-original.png` is the original 202×88 PNG, downloaded without transformation from:
https://eclipseiq.ca/wp-content/uploads/2025/04/EclipseIQ-Logo-202-x-88-px.png

Verified against WordPress media record 183. SHA-256:
`e9edbbf8165884a95bdbf18d2a7007b911fbaf35306d39c65a42bb1036b4b9fd`

The actual black/blue lettering, blue symbol, grey tagline and white background are preserved. It is displayed at or below original dimensions in header/footer and at intrinsic size in the sharing card. Favicon references the same original PNG, rather than inventing a substitute mark. No inversion, tracing, cropping, recolouring or recreated logo.

## Brand colours

Live homepage CSS explicitly uses deep blue `#023047`, turquoise `#219ebc`, white `#FFFFFF` and dark `#111111`. Original-logo opaque pixel counts identify its blue as `#13A8FF`. These values form the redesign's palette. Supporting accessible text blues (`#07688b`, `#087bad`) and pale surfaces complement these colours. The brightest original blue and turquoise are accents, not body text on white where contrast would be insufficient.

## Fonts

Source declares IBM Plex Sans and IBM Plex Sans Condensed. Self-hosted Latin WOFF2 assets from Fontsource package version 5.2.6:
- https://cdn.jsdelivr.net/npm/@fontsource/ibm-plex-sans@5.2.6/files/ibm-plex-sans-latin-400-normal.woff2
- https://cdn.jsdelivr.net/npm/@fontsource/ibm-plex-sans@5.2.6/files/ibm-plex-sans-latin-500-normal.woff2
- https://cdn.jsdelivr.net/npm/@fontsource/ibm-plex-sans@5.2.6/files/ibm-plex-sans-latin-600-normal.woff2
- https://cdn.jsdelivr.net/npm/@fontsource/ibm-plex-sans-condensed@5.2.6/files/ibm-plex-sans-condensed-latin-500-normal.woff2

SIL Open Font License included as `assets/fonts/OFL-Plex.txt`. No third-party font requests at runtime.

## Existing-site editorial image

`assets/insurance-collaboration.png` is the unmodified original:
https://eclipseiq.ca/wp-content/uploads/2024/09/EIS_BrainStorming.png

800×534, reused as general working-discussion imagery with descriptive alt text. It is not identified as the company's team, a client or an office. Its existence on the owner's live site supports reuse in the redesign; no broader licensing claim is made. Confirm original licensing at launch if not already recorded by the owner.

The historical EclipseSME landing screenshot was downloaded and reviewed during the audit but not included in the site. It contains dated illustrative metrics and old marketing UI, so it is not presented as a current interface or company result. No assets copied from the EclipseSME GitHub repository.

## New artwork

The CSS architecture illustration is a conceptual relationship between strategy, systems and insurance operations. It is not a product UI, company logo or customer architecture. Simple original inline SVG UI/service icons have no external dependencies. `assets/social.png` is a sharing composition generated from the unchanged original logo, verified colours and local fonts.
