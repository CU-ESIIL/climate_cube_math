# Stats verbs

Statistic verbs summarize cubes along dimensions or compare axes. They live in `cubedynamics.verbs` and accept whatever `xarray` object flows through the pipe.

### `v.variance(dim)`

Computes the variance along a dimension.

```python
from cubedynamics import pipe, verbs as v

result = pipe(cube) | v.variance(dim="time")
```

- **Parameters**: `dim` – dimension to collapse.
- **Returns**: variance cube with the target dimension removed (or reduced) according to `xarray` semantics.

### `v.zscore(dim="time", std_eps=1e-4)`

Standardizes each pixel/voxel along a dimension by subtracting the mean and dividing by the standard deviation.

```python
z = pipe(cube) | v.zscore(dim="time")
```

- **Parameters**: `dim`, `std_eps` – same semantics as `xarray.apply_ufunc` safeguards.
- **Notes**: Use `std_eps` to avoid division by near-zero spread.

### `v.correlation_cube(other, dim="time")`

Correlate the pipeline cube with another cube along a shared dimension.

```python
corr = (
    pipe(ndvi_z)
    | v.correlation_cube(climate_anom, dim="time")
).unwrap()
```

- **Parameters**: `other` – reference cube or DataArray; `dim` – alignment dimension.
- **Notes**: Accepts Datasets/DataArrays; returns coefficients per pixel.

### `v.rolling_corr_vs_center(window_days, min_t)`

Rolling Pearson correlation versus an anchor pixel (usually the spatial center).

```python
rolling = pipe(ndvi_z) | v.rolling_corr_vs_center(window_days=90, min_t=5)
```

- **Notes**: Output cube stores correlations aligned to the rolling window center.

### `v.rolling_tail_dep_vs_center(window_days, min_t, b=0.5)`

Tail dependence between each pixel and the anchor across rolling windows.

```python
tails = pipe(ndvi_z) | v.rolling_tail_dep_vs_center(window_days=90, min_t=5, b=0.5)
```

- **Notes**: Returns bottom, top, and difference tail dependence cubes.

Use these stats alongside transform verbs to build climate–vegetation synchrony analyses.
