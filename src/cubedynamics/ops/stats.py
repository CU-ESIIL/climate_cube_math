"""Statistical pipeable operations."""

from __future__ import annotations

import numpy as np
import xarray as xr


def variance(dim: str = "time"):
    """Factory returning a variance reducer over ``dim`` for pipe chains."""

    def _inner(da: xr.DataArray | xr.Dataset):
        if dim not in da.dims:
            raise ValueError(f"Dimension {dim!r} not found in object dims: {da.dims}")
        return da.var(dim=dim)

    return _inner


def zscore(dim: str = "time", std_eps: float = 1e-4):
    """Factory returning a z-score normalization along ``dim``."""

    def _inner(da: xr.DataArray):
        if dim not in da.dims:
            raise ValueError(f"Dimension {dim!r} not found in dims: {da.dims}")

        mean = da.mean(dim=dim, skipna=True)
        std = da.std(dim=dim, skipna=True)
        valid_std = std > std_eps

        z = xr.where(valid_std, (da - mean) / std, np.nan)
        name = da.name or "var"
        z = z.rename(f"{name}_zscore").astype("float32")
        z.attrs.update(
            {
                "long_name": f"{name} standardized anomaly (z-score)",
                "definition": f"z = (x - mean_{dim} x) / std_{dim} x",
                "baseline_dim": dim,
                "note": f"Values with std < {std_eps} set to NaN.",
            }
        )
        return z

    return _inner


def correlation_cube(other: xr.DataArray | xr.Dataset | None, dim: str = "time"):
    """Factory placeholder for a future correlation cube operation.

    Parameters
    ----------
    other:
        The comparison cube captured by the factory.
    dim:
        Dimension over which correlations would be computed once implemented.
    """

    if other is None or not isinstance(dim, str):
        raise NotImplementedError("correlation_cube is not implemented yet.")

    def _inner(da: xr.DataArray | xr.Dataset):  # pragma: no cover - stub
        raise NotImplementedError("correlation_cube is not implemented yet.")

    return _inner


__all__ = ["variance", "correlation_cube", "zscore"]
