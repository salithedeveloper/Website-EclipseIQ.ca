# EclipseIQ creative direction review

Open `index.html` in a browser to compare all three directions. Each “Open concept” button opens a complete, responsive HTML/CSS homepage. No build or package installation is needed. All design assets and screenshots are local.

For a local HTTP preview, run from the repository root:

```sh
python -m http.server 4173 --directory review/homepage-concepts
```

Then open http://localhost:4173/ in the same machine's browser. In a remote workspace use your editor's port forwarding for port 4173.

- `concept-1.html` / `concept-1.css`: **Integrated Intelligence** — recommended. The strongest expression of enterprise technical capability, with consulting and software presented as complementary parts of the business.
- `concept-2.html` / `concept-2.css`: **Executive Perspective** — an editorial, consultancy-led direction with a more human tone.
- `concept-3.html` / `concept-3.css`: **Connected Operations** — an insurance operations-led direction, using a panoramic model to make the business tangible.
- `common.css`: new concept-only typography, navigation and responsive foundations. Does not import or alter the existing implementation's stylesheet.
- `screenshots/`: full-page Chromium captures at 1440px desktop and 390px mobile widths, plus the comparison page.
- `RESEARCH.md`: source references, brand verification, asset provenance and design rationale.
- `validation.json`: browser checks across 1440, 1024, 768, 390 and 320px.
- `capture.py`: repeatable screenshot/QA helper; requires the already available Playwright Python package and `/usr/bin/chromium`, plus a local HTTP server as above.

Screenshots show conceptual illustrations, not live product interfaces. External contact/demo links lead to the current company/product sites. No deployment or internal-page build is included. Select a direction before extending the implementation.
