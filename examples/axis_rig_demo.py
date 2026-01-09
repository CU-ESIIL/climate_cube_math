"""Quick demo for verifying axis rig placement and time labels."""

from __future__ import annotations

import numpy as np
import pandas as pd
import xarray as xr

from cubedynamics import verbs as v


def make_ndvi_cube() -> xr.DataArray:
    rng = np.random.default_rng(7)
    time = pd.date_range("2022-01-01", periods=18, freq="MS")
    y = np.linspace(39.5, 40.5, 12)
    x = np.linspace(-105.8, -104.8, 12)
    data = rng.random((time.size, y.size, x.size)).astype("float32")
    return xr.DataArray(
        data,
        dims=("time", "y", "x"),
        coords={"time": time, "y": y, "x": x},
        name="ndvi",
        attrs={"long_name": "NDVI demo cube"},
    )


def main() -> None:
    cube = make_ndvi_cube()
    viewer = v.plot(cube, title="NDVI axis rig demo")
    html = viewer._repr_html_()

    output_path = "axis_rig_demo.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Wrote {output_path} for local validation.")


if __name__ == "__main__":
    main()
