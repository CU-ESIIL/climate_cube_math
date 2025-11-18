# CubeDynamics

Streaming-first climate cube math with ggplot-style piping.

## Why CubeDynamics?

- **Streaming climate cubes** assembled from PRISM, gridMET, NDVI, and other archives without local mirroring.
- **Pipe-based math** so you can write `pipe(cube) | v.anomaly() | v.variance()` and get reproducible workflows.
- **Focused verbs under `cubedynamics.verbs`** covering transforms, stats, and IO helpers for on-disk storage.

## Quickstart in a Jupyter notebook

Open a fresh notebook, install CubeDynamics, and stream a climate cube directly into the pipe system:

1. Install CubeDynamics (terminal or notebook cell):

   ```bash
   pip install cubedynamics
   # or pip install "git+https://github.com/CU-ESIIL/climate_cube_math.git@main"
   ```

2. Load a PRISM cube and run the verbs pipeline:

   ```python
   import cubedynamics as cd
   from cubedynamics import pipe, verbs as v

   cube = cd.load_prism_cube(
       lat=40.0,
       lon=-105.25,
       start="2000-01-01",
       end="2020-12-31",
       variable="ppt",
   )

   pipe(cube) \
       | v.month_filter([6, 7, 8]) \
       | v.variance(dim="time")
   ```

`pipe(value)` wraps the `xarray` object so you can forward it through verbs with the `|` operator. In notebooks the last `Pipe` expression in a cell automatically displays the wrapped DataArray/Dataset, so `.unwrap()` is optional. See [notebooks/quickstart_cubedynamics.ipynb](https://github.com/CU-ESIIL/climate_cube_math/blob/main/notebooks/quickstart_cubedynamics.ipynb) for the runnable tutorial notebook.

## Learn more

- Start with the [Getting Started guide](getting_started.md) for installation details and the first notebook pipeline.
- Dive into [Pipe Syntax & Verbs](pipe_syntax.md) to understand how each operation composes.
- Visualize cubes interactively with the [Lexcube Integration guide](lexcube.md).
- Explore the operations references when you need specifics on transforms, stats, or IO helpers.
