# CubeDynamics (`cubedynamics`)

CubeDynamics is a streaming-first climate cube math library with ggplot-style piping. It brings high-resolution climate archives (PRISM, gridMET, NDVI, and more) directly into your workflows so you can compose anomaly, synchrony, and correlation cubes without mirroring entire datasets.

## Features

- **Streaming PRISM/gridMET/NDVI climate data** for immediate analysis without bulk downloads.
- **Climate variance, correlation, trend, and synchrony cubes** that run on `xarray` objects and scale from laptops to clusters.
- **Pipe system** – build readable cube workflows with `pipe(cube) | v.anomaly() | v.variance()` syntax inspired by ggplot and dplyr.
- **Verbs namespace (`cubedynamics.verbs`)** so transforms, stats, and IO live in focused modules.
- **Cloud-ready architecture** that embraces chunked processing, lazy execution, and storage backends like NetCDF or Zarr.

## Installation

### Install from GitHub (current, recommended)

Install the `cubedynamics` package directly from the `main` branch to get the latest commits:

```bash
pip install "git+https://github.com/CU-ESIIL/climate_cube_math.git@main"
```

### Install from PyPI (future)

Once the first release is published to PyPI, installing will be as simple as:

```bash
pip install cubedynamics
```

Until that upload happens the PyPI name is reserved but unavailable.

## Quickstart

This example runs in a fresh Jupyter notebook that only has `numpy`, `pandas`, `xarray`, and `cubedynamics` installed.

```python
import numpy as np
import pandas as pd
import xarray as xr
from cubedynamics import pipe, verbs as v

# 1. Create a tiny example "cube" with a datetime coordinate
time = pd.date_range("2000-01-01", periods=12, freq="MS")
values = np.arange(12, dtype=float)

cube = xr.DataArray(
    values,
    dims=["time"],
    coords={"time": time},
    name="example_variable",
)

# 2. Run a pipe chain that computes anomalies, filters months, and gets variance
result = (
    pipe(cube)
    | v.anomaly(dim="time")
    | v.month_filter([6, 7, 8])
    | v.variance(dim="time")
).unwrap()

print("Variance of anomalies over JJA:", float(result.values))
```

### Example: stream a gridMET cube for Boulder, CO

The streaming helpers work the same way as the in-memory example above. Define an AOI, call the loader, and the resulting cube
can flow directly into the pipe system.

```python
import numpy as np
import pandas as pd
import xarray as xr
import cubedynamics as cd
from cubedynamics import pipe, verbs as v

# Define a rough AOI around Boulder, CO (lon/lat pairs in EPSG:4326)
boulder_aoi = {
    "type": "Feature",
    "properties": {"name": "Boulder, CO"},
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [-105.35, 40.00],  # SW
            [-105.35, 40.10],  # NW
            [-105.20, 40.10],  # NE
            [-105.20, 40.00],  # SE
            [-105.35, 40.00],  # back to SW
        ]],
    },
}

# Stream a monthly gridMET precipitation cube for Boulder
cube = cd.stream_gridmet_to_cube(
    aoi_geojson=boulder_aoi,
    variable="pr",
    start="2000-01-01",
    end="2020-12-31",
    freq="MS",
    chunks={"time": 120},
)

cube
```

Feed that cube into the pipe system to compute JJA variance in a single chain:

```python
jja_var = (
    pipe(cube)
    | v.month_filter([6, 7, 8])
    | v.variance(dim="time")
).unwrap()

jja_var
```

### Example: Sentinel-2 NDVI z-score cube via pipes

The verbs namespace also makes it easy to stream Sentinel-2 Level-2A data with
[`cubo`](https://github.com/carbonplan/cubo), compute NDVI, and standardize it
with a z-score transform that highlights anomalies.

```python
import warnings

import cubo
from cubedynamics import pipe, verbs as v

LAT = 43.89
LON = -102.18
START = "2023-06-01"
END = "2024-09-30"

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    s2 = cubo.create(
        lat=LAT,
        lon=LON,
        collection="sentinel-2-l2a",
        bands=["B04", "B08"],
        start_date=START,
        end_date=END,
        edge_size=512,
        resolution=10,
        query={"eo:cloud_cover": {"lt": 40}},
    )

if "band" in s2.dims and s2.dims[0] == "band":
    s2 = s2.transpose("time", "y", "x", "band")

ndvi_z = (
    pipe(s2)
    | v.ndvi_from_s2(nir_band="B08", red_band="B04")
    | v.zscore(dim="time")
).unwrap()

ndvi_z
```

### Using the pipe system

- `pipe(value)` wraps an `xarray` object in a `Pipe` so it can be chained.
- Import verbs via `from cubedynamics import verbs as v`. Calling `v.anomaly(dim="time")` returns a callable for the pipe.
- The `|` operator forwards the wrapped cube through each verb in sequence.
- `.unwrap()` returns the final `xarray` object so you can inspect the result or continue working outside the pipe.

## API Overview

- `pipe`
- `verbs` (``from cubedynamics import verbs as v``)
- `anomaly`
- `month_filter`
- `variance`
- `zscore`
- `ndvi_from_s2`
- `correlation_cube` (stub)
- `to_netcdf`

More verbs live under `cubedynamics.ops.transforms`, `cubedynamics.ops.stats`, and `cubedynamics.ops.io` and are re-exported via `cubedynamics.verbs`. Each verb returns a callable object that receives the upstream cube when used inside a pipe chain.

## Philosophy

- **Streaming-first design** – CubeDynamics emphasizes adapters that yield data as soon as it is available so analyses can begin immediately.
- **Pipe chaining** – The `Pipe` helper makes cube math declarative: each verb describes *what* to do, and the pipe handles *when* to run it.
- **xarray-compatible processing** – Every verb consumes/produces `xarray.DataArray` or `xarray.Dataset` objects, making it easy to interoperate with the broader ecosystem.

Visit https://cu-esiil.github.io/climate_cube_math/ for full documentation, concepts, and the latest changelog.
