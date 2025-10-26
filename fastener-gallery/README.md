# Fastener Explorer

A lightweight, static web app that lets you browse different manufacturing
fasteners, view illustrations, and see sample FreeCAD commands for generating
reference models.

## Features

- Interactive fastener selector with descriptive copy and typical use cases
- Specification snapshot table and Python command snippet per fastener
- SVG illustrations that keep the page lightweight and easy to customize
- A companion `python_fastener_export.py` script that can be run inside
  FreeCAD's Python console/CLI to export parametric STEP/STL previews

## Getting started

1. Open `index.html` in any modern browser. The page is fully client-side and
   does not require a build step.
2. Use the dropdown to pick a fastener. The description, applications, and
   exported FreeCAD command will update automatically.
3. Replace the illustrative SVGs in `assets/fasteners/` with your own exports if
   desired.

## Generating models with FreeCAD

1. Launch the FreeCAD command-line interpreter (`freecadcmd`).
2. Run the helper script with the desired fastener and parameters (from within
   the `python/` subfolder or by passing the relative path):

   ```bash
   cd python
   freecadcmd python_fastener_export.py --fastener hex_bolt --diameter 12 --length 45
   ```

3. The script exports both `.step` and `.stl` files under the `exports/`
   directory by default. Use these to create renders, convert to glTF, or feed
   them into other visualization pipelines.
4. Update the SVG preview or integrate a web-based 3D viewer (such as Three.js)
   to display your generated files.

## Customizing the UI

- Modify `app.js` to add or remove fastener definitions, tweak the descriptive
  metadata, or change the command snippets.
- Update `styles.css` for branding changes, layout adjustments, or to wire the
  page into a larger design system.

## Folder layout

```
fastener-gallery/
├── index.html            # UI layout
├── styles.css            # Styling for the gallery
├── app.js                # Fastener data + rendering logic
├── assets/fasteners/     # SVG illustrations
└── python/               # FreeCAD export helper
```
