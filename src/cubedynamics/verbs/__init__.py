"""Namespace exposing pipe-friendly cube verbs."""

from __future__ import annotations

from ..ops.io import to_netcdf
from ..ops.ndvi import ndvi_from_s2
from ..ops.stats import correlation_cube, variance, zscore
from ..ops.transforms import anomaly, month_filter

__all__ = [
    "anomaly",
    "month_filter",
    "variance",
    "correlation_cube",
    "to_netcdf",
    "zscore",
    "ndvi_from_s2",
]
