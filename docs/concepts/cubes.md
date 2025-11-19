# What is a cube?

A **cube** is an `xarray.DataArray` or `xarray.Dataset` whose values are organized along shared space-time axes such as `(time, y, x)` for single-band cubes or `(time, y, x, band)` for multispectral collections. Every pixel stores the value of an environmental variable (e.g., NDVI, temperature, precipitation) measured at `(y, x)` and instant `time`.

![Cube axes diagram](../assets/img/cube_axes.png){ .cube-image }

## Loading a PRISM cube

```python
import cubedynamics as cd

cube = cd.load_prism_cube(
    lat=40.0,
    lon=-105.25,
    start="2000-01-01",
    end="2020-12-31",
    variable="ppt",
)

cube
```

`load_prism_cube` streams the requested area/time window from PRISM into memory as a cube so you can immediately apply verbs. Swap in `load_gridmet_cube`, `load_sentinel2_ndvi_cube`, or any custom loader that returns an `xarray` object with the standard axes.

## Why cubes?

Satellite constellations (Sentinel-2, Landsat), gridded climate products (gridMET, PRISM), and model reanalyses naturally produce cube-shaped data because measurements are already tied to regular spatiotemporal coordinates. By sticking with `xarray`, CubeDynamics benefits from labeled dimensions, lazy loading (`dask`), and metadata-aware computations.

CubeDynamics focuses on **streaming cubes** instead of requiring large local downloads. Utilities such as `cubedynamics.data.sentinel2.load_s2_cube` wrap remote APIs (e.g., Cubo) so you can request an area/time window and immediately operate on the returned cube in notebooks or scripts.

## Cube processing layers

The original documentation described four conceptual layers that remain relevant today:

1. **Data layer** – load space-time cubes (`load_s2_cube`, `load_prism_cube`, `load_gridmet_cube`).
2. **Indices & anomalies layer** – derive vegetation indices and z-scores (`from cubedynamics import verbs as v`; `v.ndvi_from_s2`, `v.zscore`, `v.anomaly`).
3. **Synchrony layer** – measure rolling correlation and tail dependence versus a reference pixel (`v.correlation_cube`, `rolling_corr_vs_center`, `rolling_tail_dep_vs_center`).
4. **Visualization layer** – explore cubes interactively with the Lexcube widget (`v.show_cube_lexcube`) and QA plots (`plot_median_over_space`).

## Earth System Data Cube context

CubeDynamics builds on the Earth System Data Cube (ESDC) paradigm: treat spatiotemporal grids as analysis-ready cubes that can flow into machine learning or statistical analyses. Unlike infrastructure-focused systems (Open Data Cube, Earth System Data Lab), CubeDynamics emphasizes a **grammar of analysis**. Any cube—PRISM, gridMET, Sentinel-2 NDVI via Cubo, Lexcube outputs, or DeepESDL—becomes a first-class citizen in the same `pipe(cube) | verbs` interface.
