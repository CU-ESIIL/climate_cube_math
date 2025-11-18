# Climate cube math primitives

The `climate_cube_math` package collects reusable *cube math* primitives that
operate directly on `xarray` objects without breaking their labeled dimensions.
These primitives fall into three categories.

## Temporal operations

- **Z-scores & anomalies** – `stats.anomalies.zscore_over_time` and related
  helpers standardize or demean each pixel.
- **Rolling reductions** – `stats.rolling` defines moving-window statistics that
  are later specialized by the correlation/tail modules.
- **Lag/lead transforms** – differencing, smoothing, and other future helpers can
  be layered on time-centered cubes to highlight rate-of-change or persistence.

## Spatial operations

- **Coarsening & striding** – `utils.chunking.coarsen_and_stride` reduces spatial
  resolution and sub-samples time for performance.
- **Masks & neighborhoods** – boolean masks (e.g., from QA bands or external
  polygons) can gate where calculations run. Neighborhood operations such as
  smoothing or gradients preserve the `y`/`x` axes while aggregating across
  nearby pixels.

## Metadata conventions

All primitives expect the standard `(time, y, x)` dimension order (with optional
band/variable axis). Coordinates should be named `time`, `y`, `x`, and any extra
bands should be labeled via the `band` or `variable` dimension. Attributes are
carried through operations so that downstream plots know the data source,
projection, or scaling applied.

## Putting it together

By composing these primitives we can:

1. Load a cube.
2. Apply temporal standardization (z-scores).
3. Reduce spatial resolution or mask invalid data.
4. Derive rolling synchrony metrics.
5. Visualize the resulting cubes via Lexcube and QA plots.

The abstraction lets you swap in other backends (e.g., GRIDMET temperature
cubes) while keeping the same math pipeline.
