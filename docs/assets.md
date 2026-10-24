# Active website assets

## Identity and typography

- `assets/eclipseiq-logo-original.png`: unchanged original 202×88 logo from https://eclipseiq.ca/wp-content/uploads/2025/04/EclipseIQ-Logo-202-x-88-px.png. SHA-256 `e9edbbf8165884a95bdbf18d2a7007b911fbaf35306d39c65a42bb1036b4b9fd`. Kept on white at or below intrinsic size; no tracing, inversion, cropping or recolouring.
- `assets/fonts/manrope.woff2`: existing self-hosted variable Manrope, used for headings. Original SIL Open Font License remains alongside it.
- `assets/fonts/ibm-plex-sans.woff2`: self-hosted variable IBM Plex Sans, obtained from https://cdn.jsdelivr.net/npm/@fontsource-variable/ibm-plex-sans/files/ibm-plex-sans-latin-wght-normal.woff2. SIL Open Font License included as `OFL-IBM-Plex-Sans.txt`. No runtime font provider.

## Commissioned imagery

- `assets/enterprise-hero.webp`: original AI-generated editorial engineering scene with code and technical documents. It is illustrative, not a photograph of an EclipseIQ office, employee or client.
- `assets/enterprise-product.webp`: original AI-generated concept render of a laptop and insurance documents. It is not a real EclipseSME screen; the visible caption and alt text identify that limitation. No made-up performance numbers, client data or product interface claims.

Generated source images remain in the execution environment's `generated_images` directory. Delivery copies preserve the source dimensions and are encoded as WebP for performance, about 174 KiB combined. No reference company's imagery is copied.

## Supporting assets

- Original inline SVG icons identify software, engineering, consulting and leadership.
- `assets/social.png`: sharing image using the actual logo, local typography and current positioning; generated with `scripts/social.py`.

Earlier photographs, standalone document SVG and historical concept assets remain in the repository but are not dependencies of the active layouts. Blue/turquoise branding remains, with deep navy surfaces, `#219ebc` turquoise and the original logo blue.
