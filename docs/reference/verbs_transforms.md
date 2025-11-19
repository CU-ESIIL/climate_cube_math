# Transform verbs

Transform verbs reshape or filter cubes before you compute downstream statistics. All functions live under `cubedynamics.verbs` and can be chained via `pipe(cube) | v.verb(...)`.

### `v.anomaly(dim="time")`

Compute anomalies by subtracting the mean along a given dimension. The output keeps the same shape as the input cube so Lexcube visualization remains valid.

```python
from cubedynamics import pipe, verbs as v

anom = (
    pipe(cube)
    | v.anomaly(dim="time")
).unwrap()
```

- **Parameters**: `dim` – dimension name (e.g., `"time"`).
- **Notes**: Preserves metadata and alignment across coordinates.

### `v.month_filter(months)`

Filter the cube to only certain calendar months. The verb drops timesteps outside the requested month list.

```python
jja = pipe(cube) | v.month_filter([6, 7, 8])
```

- **Parameters**: `months` – iterable of month numbers (1–12).
- **Notes**: Requires a datetime-like `time` coordinate.

### `v.ndvi_from_s2(nir_band="B08", red_band="B04")`

Derive NDVI from Sentinel-2 reflectance cubes. The incoming object must expose a `band` dimension containing the requested near-infrared (`nir_band`) and red (`red_band`) entries. The verb returns a `(time, y, x)` NDVI cube with float32 reflectance values in `[-1, 1]`.

```python
ndvi = (
    pipe(s2_cube)
    | v.ndvi_from_s2()
).unwrap()
```

- **Parameters**: `nir_band`, `red_band` – band names present in the cube.
- **Notes**: Works with cubes loaded via `cd.load_sentinel2_cube` (legacy alias `load_s2_cube`) or `cubo.create`.

Use these verbs as building blocks ahead of stats like variance or correlation. Rolling synchrony helpers such as `cubedynamics.rolling_corr_vs_center` and `cubedynamics.rolling_tail_dep_vs_center` live outside the `verbs` namespace.
