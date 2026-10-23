# Natural captures and reversible breakaway

2026-10-24.

- Replaced the ten-image set with ten reviewed captures of naturally generated river terrain, forest, underwater banks, riverbed and sky. No material slabs, constructed waterfalls, test platforms or menus are selected.
- Original captures and the previous selection remain intact. `tools/curate_natural_showcase.py` rebuilds the new selection and static fallback assets from the existing captures, checks original SHA-256 hashes and compares every shader runtime file against the packaged 1.6.10 release. Capture settings are labelled individually; no new Minecraft run or FPS result is claimed.
- Automatic publication still follows the full-version-ending-in-0 rule. It now requires exactly ten distinct reviewed natural-world images with matching checksums and release runtime confirmation. A later release without such a set preserves the existing gallery.
- Hero imagery separates into twelve decorative tiles; real section pieces translate and rotate apart as their section scrolls out. Scroll progress determines state, so scrolling up reassembles them. No scroll interception or artificial scrolling is used.
- Header, feedback inputs and private Studio access remain functional and outside decorative fragments. Keyboard-focused content is kept stable. Motion OFF and reduced-motion settings disable the breakaway.

## Observed checks

- Inspected all ten selected images together: natural scenes, without test platforms or HUD overlays.
- Live publication API returned version 1.6.10 and ten natural-world scene titles.
- Preview hero break progress increased to 0.4933 while scrolling down and returned to 0.0000 after scrolling back up; screenshots reviewed at both positions.
- Preview registered 39 breakaway groups and twelve hero tiles while retaining ten gallery scenes.
- Mobile distances are reduced through responsive CSS; physical-device verification remains unperformed.
