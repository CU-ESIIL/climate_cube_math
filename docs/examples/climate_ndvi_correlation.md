# Climate–NDVI correlation cube

Correlation cubes capture how vegetation anomalies co-vary with climate drivers. This example merges the earlier correlation notes with the new pipe-first grammar.

## Load climate and NDVI cubes

```python
import cubedynamics as cd
from cubedynamics import pipe, verbs as v

prism_cube = cd.load_prism_cube(
    lat=40.0,
    lon=-105.25,
    start="2000-01-01",
    end="2020-12-31",
    variable="ppt",
)

ndvi_z = cd.load_sentinel2_ndvi_cube(
    lat=40.0,
    lon=-105.25,
    start="2018-01-01",
    end="2020-12-31",
)
```

## Prepare anomalies

```python
climate_anom = (
    pipe(prism_cube)
    | v.anomaly(dim="time")
).unwrap()
```

## Compute correlation cube

```python
corr = (
    pipe(ndvi_z)
    | v.correlation_cube(climate_anom, dim="time")
).unwrap()
```

The output stores correlation coefficients per pixel, aligned along the `time` coordinate (full-period or rolling depending on the configuration). Use it to spot areas where vegetation responds strongly to precipitation anomalies.

## Rolling correlation vs anchor pixels

`v.rolling_corr_vs_center` and `v.rolling_tail_dep_vs_center` extend the idea to within-cube synchrony (e.g., NDVI vs center pixel). They inherit the same pipe syntax:

```python
rolling = (
    pipe(ndvi_z)
    | v.rolling_corr_vs_center(window_days=90, min_t=5)
)
```

## Related documentation

- [Correlation & synchrony cubes](../correlation_cubes.md)
- [Sentinel-2 NDVI z-score cube](s2_ndvi_zscore.md)
- [Verbs – Stats](../reference/verbs_stats.md)
