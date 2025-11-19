# IO verbs

IO verbs move cubes to disk or other systems without breaking the pipe chain.

### `v.to_netcdf(path)`

Writes the upstream cube to a NetCDF file.

```python
from pathlib import Path
from cubedynamics import pipe, verbs as v

path = Path("out.nc")
pipe(cube) \
    | v.anomaly(dim="time") \
    | v.to_netcdf(path)
```

- **Parameters**: `path` – output path.
- **Behavior**: saves the cube to NetCDF and returns the original object so you can continue chaining if desired.

### `v.to_zarr(path, mode="w")` (planned)

A forthcoming exporter for chunked cloud storage. Follow the [Roadmap](../dev/roadmap.md) for progress updates.

Use `to_netcdf` at the end of a pipe to persist results, or in the middle if you want to checkpoint intermediate artifacts.
