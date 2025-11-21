import numpy as np
import pandas as pd
import xarray as xr

from cubedynamics import verbs as v
from cubedynamics.plotting import CubePlot


def test_plot_returns_cubeplot_from_direct_call():
    times = pd.date_range("2024-01-01", periods=3, freq="D")
    data = xr.DataArray(
        np.ones((3, 2, 2)),
        coords={"time": times, "y": [0, 1], "x": [0, 1]},
        dims=("time", "y", "x"),
        name="test",
    )

    result = v.plot()(data)

    assert isinstance(result, CubePlot)
