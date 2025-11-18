"""Tests for anomaly utilities."""

from __future__ import annotations

import numpy as np
import xarray as xr

from climate_cube_math.config import STD_EPS
from climate_cube_math.stats.anomalies import zscore_over_time


def test_zscore_over_time_basic(tiny_cube: xr.DataArray) -> None:
    z = zscore_over_time(tiny_cube, dim="time", std_eps=STD_EPS)

    assert z.shape == tiny_cube.shape
    assert z.dims == tiny_cube.dims

    mean = z.mean(dim="time", skipna=True)
    std = z.std(dim="time", skipna=True)

    assert np.all(np.isfinite(mean))
    assert np.all(np.isfinite(std))

    max_abs_mean = float(np.abs(mean).max())
    max_std_dev = float(np.abs(std - 1.0).max())
    assert max_abs_mean < 1e-2
    assert max_std_dev < 1e-2


def test_zscore_over_time_std_eps_masks_flat_series() -> None:
    time = np.arange(5)
    y = np.arange(2)
    x = np.arange(2)
    data = np.ones((len(time), len(y), len(x)), dtype=float)
    da = xr.DataArray(data, coords={"time": time, "y": y, "x": x}, dims=("time", "y", "x"))

    z = zscore_over_time(da, dim="time", std_eps=1e-4)
    assert np.isnan(z).all()
