# Testing reconstruction & QA patterns

These notes collect reconstruction and QA checks used when validating cube-building utilities, viewer outputs, and spatial joins.

- **Geometry and CRS sanity**: Confirm datasets satisfy the [Spatial & CRS Dataset Contract](../design/spatial_dataset_contract.md) before composing them. Dimension naming, CRS detection, and alignment are part of the expected fixture setup for new tests.
- **Provenance inspection**: Cube outputs should carry `source`, `is_synthetic`, `freq`, and CRS metadata. Assert these in tests when comparing downloaded vs. synthetic fallbacks.
- **Round-trips**: When verbs write/read intermediate artifacts (e.g., zarr, parquet, NetCDF), prefer lightweight round-trip tests that ensure attributes and chunking survive.
- **Viewer reconstruction**: For viewer-facing helpers, include checks that meshes/hulls reconstruct expected shapes (vertex counts, bounding boxes, monotonic time) and that color limits derive from data rather than hard-coded values.

Use these patterns to expand integration suites without pulling heavy data into the unit path.
