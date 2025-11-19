# Operations Reference – Stats

Statistic verbs summarize cubes along dimensions or compare axes. They live in `cubedynamics.ops.stats` and are re-exported via `cubedynamics.verbs`. Examples assume `from cubedynamics import pipe, verbs as v` and a `cube` variable bound to an `xarray` object.

## `mean(dim="time", keep_dim=True)`

Compute the mean along a dimension.

```python
result = pipe(cube) | v.mean(dim="time", keep_dim=True)
```

- **Parameters**
  - `dim`: dimension to summarize.
  - `keep_dim`: retain the dimension as length 1 (default) or drop it entirely.

## `variance(dim="time", keep_dim=True)`

Compute the variance along a dimension.

```python
result = pipe(cube) | v.variance(dim="time", keep_dim=True)
```

- **Parameters**
  - `dim`: dimension to collapse.
  - `keep_dim`: retain the dimension as length 1 (default) or drop it entirely.
- **Returns**: variance cube matching the input layout when `keep_dim=True`.

## `zscore(dim="time", std_eps=1e-4)`

Standardize each pixel/voxel along a dimension by subtracting the mean and dividing by the standard deviation.

```python
result = pipe(cube) | v.zscore(dim="time")
```

- **Parameters**
  - `dim`: dimension to standardize along.
  - `std_eps`: mask threshold to avoid dividing by values with near-zero spread.
- **Returns**: anomaly cube whose values are unitless z-scores per pixel. The verb always preserves the original cube shape.

## `correlation_cube` (planned)

The exported factory currently raises `NotImplementedError` and is reserved for a future streaming implementation.

- **Intended behavior**: compute rolling or full-period correlations between named data variables or coordinates, returning an `xarray` cube with correlation coefficients.
- **Alternatives today**: use `xr.corr` for per-pixel correlations or the rolling helpers in `cubedynamics.stats.correlation`/`stats.tails`.

Combine these stats with transforms and IO verbs to produce complete analyses.
