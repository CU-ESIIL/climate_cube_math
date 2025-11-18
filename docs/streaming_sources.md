# Streaming PRISM & gridMET

CubeDynamics treats climate data sources as interchangeable **streaming
backends**. Each loader returns a cube with identical axes and metadata so the
rest of the math stack can focus on statistics.

## PRISM

- Loader: `cubedynamics.stream_prism_to_cube`
- Purpose: high-resolution precipitation and temperature summaries
- Strategy: use STAC manifests and HTTP range requests to read only the pixels
  covering your AOI and date window

```python
cube = cubedynamics.stream_prism_to_cube(
    aoi_geojson,
    variable="ppt",
    dates=("2015-01-01", "2020-12-31"),
)
```

## gridMET

- Loader: `cubedynamics.stream_gridmet_to_cube`
- Purpose: daily meteorological drivers (temperature, precipitation, vapor
  pressure deficit)
- Strategy: chunked downloads over object storage, falling back to cached tiles
  when streaming is unavailable

```python
boulder_aoi = {
    "type": "Feature",
    "properties": {"name": "Boulder, CO"},
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [-105.35, 40.00],
            [-105.35, 40.10],
            [-105.20, 40.10],
            [-105.20, 40.00],
            [-105.35, 40.00],
        ]],
    },
}

cube = cubedynamics.stream_gridmet_to_cube(
    aoi_geojson=boulder_aoi,
    variable="pr",
    start="2000-01-01",
    end="2020-12-31",
    freq="MS",
    chunks={"time": 120},
)
```

## Sentinel-2 / NDVI

Sentinel-2 reflectance cubes feed vegetation indices and QA workflows.
`stream_sentinel2_to_cube` requests chips from providers such as Cubo or the
Planetary Computer, then the `cubedynamics.verbs.ndvi_from_s2` verb transforms
them into NDVI cubes for downstream cube math.

## Custom sources

Each loader implements the same contract: accept AOI geometry, variables, dates,
and streaming hints; return an `xarray` cube. Follow the existing modules to add
new sources (e.g., ERA5, SMAP) without changing downstream notebooks.
