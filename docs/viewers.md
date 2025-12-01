# Cube viewers

## Standalone HTML cube viewer

Generate a fully offline, self-contained cube viewer using:

```python
from cubedynamics.viewers import write_cube_viewer

write_cube_viewer(ndvi, "ndvi_cube.html")
```

The output HTML bundles all JavaScript and textures so it can be opened directly in
a browser or embedded into a notebook with `IFrame("ndvi_cube.html", width=900, height=900)`.

### Mouse/trackpad controls

- **Rotate:** click-and-drag anywhere in the cube frame (faces or the transparent padding). The drag surface captures the pointer so rotation keeps flowing even if the cursor leaves the canvas mid-drag.
- **Zoom:** use a trackpad pinch gesture or mouse scroll to zoom the cube in/out.
- **Reset view:** rerun the cell or reload the saved HTML; the cube opens with the initial azimuth/elevation set in `coord_cube`.
