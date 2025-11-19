# Roadmap

This roadmap reflects near-term development priorities plus longer-term ambitions for CubeDynamics.

## Near term

- **Stabilize loaders** – polish `load_prism_cube`, `load_gridmet_cube`, and `load_sentinel2_ndvi_cube` with clearer AOI validation and chunk hints.
- **Reference verbs** – fill out stats/transform IO docs and ensure every helper has an example in the new `reference/` section.
- **Sentinel-2 notebooks** – keep the NDVI z-score tutorial in sync with the docs, including Lexcube screenshots and Binder links.
- **Correlation cubes** – graduate `v.correlation_cube` and rolling correlation verbs from stubs to tested implementations.

## Mid term

- **IO expansion** – add `v.to_zarr`/`v.to_geotiff` exporters plus metadata helpers for catalog integration.
- **Visualization palette** – expose more QA plot verbs (`quick_map`, `hist_over_time`) using the new color scheme.
- **Model verbs** – prototype cube-aware regression/classification verbs that emit predictions in cube form.

## Long term

- **Catalog integration** – connect to ESDC, Open Data Cube, and DeepESDL catalogs so users can pull remote cubes via a unified interface.
- **Storage backends** – optional local stores (Zarr + Parquet metadata) for caching repeated AOI requests.
- **Community examples** – curated gallery of climate–vegetation analyses contributed by the community.
