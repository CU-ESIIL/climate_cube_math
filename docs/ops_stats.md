# Operations Reference – Stats

Statistic verbs summarize cubes along dimensions or compare axes. They live in `cubedynamics.ops.stats` and are re-exported via `cubedynamics.verbs`. Examples assume `from cubedynamics import pipe, verbs as v` and a `cube` variable bound to an `xarray` object.

## `variance(dim)`

Computes the variance along a dimension.

```python
result = pipe(cube) | v.variance(dim="time")
```

## `zscore(dim="time", std_eps=1e-4)`

Standardizes each pixel/voxel along a dimension by subtracting the mean and dividing by the standard deviation.

```python
result = pipe(cube) | v.zscore(dim="time")
```

- **Parameters**
  - `dim`: dimension to standardize along.
  - `std_eps`: mask threshold to avoid dividing by values with near-zero spread.
- **Returns**: anomaly cube whose values are unitless z-scores per pixel.

- **Parameters**
  - `dim`: dimension to collapse.
- **Returns**: variance cube with the target dimension removed (or reduced) according to `xarray` semantics.

## `correlation_cube` (stub)

A forthcoming verb for building correlation matrices/surfaces between variables, time windows, or anchor pixels.

```python
result = pipe(cube) | v.correlation_cube(target="ndvi", reference="pr")
```

- **Intended behavior**: compute rolling or full-period correlations between named data variables or coordinates, returning an `xarray` cube with correlation coefficients.
- **Status**: interface stub; functionality will land alongside streaming adapters.

Combine these stats with transforms and IO verbs to produce complete analyses.
