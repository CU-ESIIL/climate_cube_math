# Transform verbs

Transform verbs reshape or filter cubes before you compute downstream statistics. All functions live under `cubedynamics.verbs` and can be chained via `pipe(cube) | v.verb(...)`.

### `v.anomaly(dim="time")`

Compute anomalies by subtracting the mean along a given dimension.

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

Filter the cube to only certain calendar months.

```python
jja = pipe(cube) | v.month_filter([6, 7, 8])
```

- **Parameters**: `months` – iterable of month numbers (1–12).
- **Notes**: Requires a datetime-like `time` coordinate.

### `v.ndvi_from_s2(nir_band="B08", red_band="B04")`

Derive NDVI from Sentinel-2 reflectance cubes.

```python
ndvi = (
    pipe(s2_cube)
    | v.ndvi_from_s2()
).unwrap()
```

- **Parameters**: `nir_band`, `red_band` – band names present in the cube.
- **Notes**: Works with cubes loaded via `cd.load_s2_cube` or `cubo.create`.

### `v.rolling_corr_vs_center(window_days, min_t)`

Compute rolling correlations between each pixel and the center/anchor pixel.

```python
rolling = (
    pipe(ndvi_z)
    | v.rolling_corr_vs_center(window_days=90, min_t=5)
)
```

- **Parameters**: `window_days` – rolling window size; `min_t` – minimum observations per window.
- **Notes**: Produces a cube aligned to the rolling window center.

### `v.rolling_tail_dep_vs_center(window_days, min_t, b=0.5)`

Measure asymmetric tail dependence relative to an anchor pixel.

```python
 tails = (
     pipe(ndvi_z)
     | v.rolling_tail_dep_vs_center(window_days=90, min_t=5, b=0.5)
 )
```

- **Notes**: Returns bottom, top, and difference tail dependence cubes for Lexcube visualization.

Use these verbs as building blocks ahead of stats like variance or correlation.
