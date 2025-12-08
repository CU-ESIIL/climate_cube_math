# NDVI cube viewer in notebooks

This minimal example renders the interactive cube viewer inside a trusted Jupyter notebook.
The viewer writes a standalone HTML snapshot to disk and loads it via an iframe so JavaScript
remains enabled even when the notebook sanitizes inline scripts.

```python
import cubedynamics as cd
from cubedynamics import pipe, verbs as v

ndvi = cd.ndvi(
    lat=40.0,
    lon=-105.25,
    start="2023-01-01",
    end="2024-12-31",
)

pipe(ndvi) | v.plot()
```

Trust the notebook cell output to enable full interactivity (drag to rotate, scroll to zoom).
You can also open the generated `cube_viewer_*.html` file directly from the working directory
if you want to share a static snapshot.
