# Asset provenance and branding

## Corporate logo

`assets/eclipseiq-logo-original.png` is the original 202×88 PNG, downloaded without transformation from:
https://eclipseiq.ca/wp-content/uploads/2025/04/EclipseIQ-Logo-202-x-88-px.png

Verified against WordPress media record 183. SHA-256:
`e9edbbf8165884a95bdbf18d2a7007b911fbaf35306d39c65a42bb1036b4b9fd`

The actual black/blue lettering, blue symbol, grey tagline and white background are preserved. It is displayed at or below original dimensions in header/footer and at intrinsic size in the sharing card. Favicon references the same original PNG, rather than inventing a substitute mark. No inversion, tracing, cropping, recolouring or recreated logo.

## Brand colours

Live homepage CSS explicitly uses deep blue `#023047`, turquoise `#219ebc`, white `#FFFFFF` and dark `#111111`. Original-logo opaque pixel counts identify its blue as `#13A8FF`. These values form the redesign's palette. Supporting accessible text blues (`#07688b`, `#087bad`) and pale surfaces complement these colours. The brightest original blue and turquoise are accents, not body text on white where contrast would be insufficient.

## Typography

The current creative direction uses a self-hosted variable Manrope font (weights 200–800), downloaded from:
https://cdn.jsdelivr.net/npm/@fontsource-variable/manrope/files/manrope-latin-wght-normal.woff2

SIL Open Font License included at `assets/fonts/OFL-Manrope.txt`. No runtime external font requests. The source website's IBM Plex fonts were verified during the live audit but are no longer used or shipped. Typography is a new design decision, not a claim about the original site.

## Retired imagery and artwork

The original site's EIS_BrainStorming photograph and historical EclipseSME landing screenshot were reviewed in the live audit. Neither is shipped in the new direction. The photo-based about section, stacked-layer CSS artwork, icon cards and all gradients were removed. Their provenance remains in the historical audit, not as current design guidance.

## Sharing image and icons

`assets/social.png` uses the new editorial typography and unchanged original logo. Generate with `scripts/social.py` using locally fulfilled font/logo requests. Simple original inline SVG arrow, menu and disclosure icons support navigation; no third-party icon package or decorative illustrations.
