# Climate Cube Math

This repository is intentionally small: it holds a minimal MkDocs website, a
Python package, and a vignette notebook that demonstrate how to generate ruled
surfaces from simplified fire-event polygons.  Everything else that shipped with
the original training template has been removed so new work can focus on the
package and the documentation that explains it.

## Quick start

```bash
# create a virtual environment however you like, then install the project
python -m pip install -e .

# open the vignette in JupyterLab or VS Code
jupyter lab docs/vignette.ipynb
```

The Python package exposes two helpers:

* `climate_cube_math.make_demo_event()` builds a small GeoDataFrame that mimics
  how a fire perimeter evolves through time.
* `climate_cube_math.plot_ruled_time_hull()` converts that data into a 3D ruled
  surface so the temporal pattern can be inspected visually.

## Documentation and vignette

The public website is generated from the `docs/` folder using MkDocs Material
and includes:

1. A concise landing page that explains the project goals.
2. A rendered copy of `docs/vignette.ipynb` so visitors can step through the
   example without leaving the site.
3. An API reference driven by `mkdocstrings` that documents the two helper
   functions shipped with the package.

To preview the site locally run:

```bash
mkdocs serve
```

## Repository layout

```
climate_cube_math/   # installable Python package
  demo.py            # demo GeoDataFrame generator
  hulls.py           # ruled time hull plotting helper
  __init__.py

docs/
  index.md           # landing page
  api.md             # mkdocstrings API reference
  vignette.ipynb     # notebook rendered on the site
  stylesheets/
    extra.css        # small cosmetic tweaks for MkDocs Material

.github/workflows/pages.yml  # deploys the docs site to GitHub Pages
mkdocs.yml                   # MkDocs configuration
pyproject.toml               # package metadata
```

With this layout you only need to touch two places when extending the project:
add or update Python modules inside `climate_cube_math/` and describe those
changes through Markdown or notebooks in `docs/`.
