# Stats verbs

Statistic verbs summarize cubes along dimensions or compare axes. They live in `cubedynamics.verbs` and accept whatever `xarray` object flows through the pipe.

### `v.mean(dim="time", keep_dim=True)`

Compute the mean along a dimension.

```python
from cubedynamics import pipe, verbs as v

mean_cube = pipe(cube) | v.mean(dim="time", keep_dim=True)
```

- **Parameters**: `dim` – dimension to summarize; `keep_dim` – retain the dimension as length 1 so the result stays `(time, y, x)` and Lexcube-ready.
- **Notes**: When `keep_dim=False`, the reduced dimension is removed entirely.

### `v.variance(dim="time", keep_dim=True)`

Compute the variance along a dimension.

```python
from cubedynamics import pipe, verbs as v

var_cube = pipe(cube) | v.variance(dim="time", keep_dim=True)
```

- **Parameters**: `dim` – dimension to collapse; `keep_dim` – retain the reduced axis (length 1) or drop it.
- **Returns**: variance cube matching the input layout when `keep_dim=True`.

### `v.zscore(dim="time", std_eps=1e-4)`

Standardizes each pixel/voxel along a dimension by subtracting the mean and dividing by the standard deviation. The verb always returns the same shape as the input cube so downstream visualization works without extra reshaping.

```python
z = pipe(cube) | v.zscore(dim="time")
```

- **Parameters**: `dim`, `std_eps` – same semantics as `xarray` reductions. `std_eps` prevents division by near-zero spread.
- **Notes**: Keeps the original cube shape regardless of `keep_dim`.

### `v.correlation_cube(other, dim="time")` (planned)

`v.correlation_cube` currently raises `NotImplementedError` and is reserved for a future streaming implementation. Use `xr.corr` or the rolling helpers under `cubedynamics.stats` today:

```python
import xarray as xr

corr = xr.corr(ndvi_z, climate_anom, dim="time")
```

Rolling synchrony functions such as `cubedynamics.rolling_corr_vs_center` and `cubedynamics.rolling_tail_dep_vs_center` live outside the verbs namespace.

Use these stats alongside transform verbs to build climate–vegetation synchrony analyses.
