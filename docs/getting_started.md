# Getting Started

CubeDynamics (`cubedynamics`) runs anywhere `xarray` does—laptops, clusters, or hosted notebooks. Use this guide to install the package, spin up the first pipe chain, and know where the notebook vignette lives.

## Installation

### Install from GitHub today

Grab the latest commits straight from the main branch. Installing inside a virtual environment (via `venv` or Conda) is recommended but optional.

```bash
pip install "git+https://github.com/CU-ESIIL/climate_cube_math.git@main"
```

### Install from PyPI once released

As soon as the first release is uploaded to PyPI you will be able to run:

```bash
pip install cubedynamics
```

Until then, use the GitHub install above for the working package.

## First pipeline in a notebook

1. Install CubeDynamics in your notebook environment (see the command above).
2. Create a tiny in-memory cube. In CubeDynamics a “cube” is simply an `xarray.DataArray` or `xarray.Dataset` that carries time/space coordinates.
3. Chain a few verbs with the pipe syntax:

```python
import numpy as np
import pandas as pd
import xarray as xr
from cubedynamics import pipe, verbs as v

# 1D time series cube with a datetime coordinate – works for multi-dimensional data too
time = pd.date_range("2000-01-01", periods=12, freq="MS")
values = np.arange(12, dtype=float)

cube = xr.DataArray(
    values,
    dims=["time"],
    coords={"time": time},
    name="example_variable",
)

result = (
    pipe(cube)
    | v.anomaly(dim="time")
    | v.month_filter([6, 7, 8])
    | v.variance(dim="time")
).unwrap()

float(result.values)
```

This pipeline is dimension-agnostic—the verbs accept any axes you provide. The `.unwrap()` call returns the final `xarray` object so it behaves like any other DataArray.

## Beyond the minimal example

- Read the [Pipe Syntax & Verbs](pipe_syntax.md) page for more callables such as `month_filter`, `to_netcdf`, and how to author your own verbs.
- Explore future climate streaming examples (PRISM/gridMET/NDVI) as they land in the docs and notebooks.
- Run the full [CubeDynamics Quickstart notebook](https://github.com/CU-ESIIL/climate_cube_math/blob/main/notebooks/quickstart_cubedynamics.ipynb) for a ready-made walkthrough that matches this guide.

## Streaming a gridMET cube for Boulder, CO

Copy/paste the snippet below into a notebook cell to stream a monthly precipitation cube straight into `xarray`:

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

Use the cube inside a pipe chain immediately:

```python
jja_var = (
    pipe(cube)
    | v.month_filter([6, 7, 8])
    | v.variance(dim="time")
).unwrap()

jja_var
```
