"""Streaming helpers for gridMET data sources."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import xarray as xr

from .data.gridmet import load_gridmet_cube


def stream_gridmet_to_cube(
    aoi_geojson: dict,
    variable: str,
    start: str,
    end: str,
    *,
    source: str = "gridmet",
    freq: str = "MS",
    chunks: dict | None = None,
    **kwargs: Any,
) -> xr.DataArray:
    """Stream a gridMET climate cube for the requested AOI and time span.

    Parameters
    ----------
    aoi_geojson:
        GeoJSON Feature or FeatureCollection describing the area of interest in
        EPSG:4326 (longitude, latitude coordinates).
    variable:
        gridMET variable name such as ``"pr"`` or ``"tmmx"``.
    start, end:
        ISO-8601 date strings that bound the time range to stream.
    source:
        Name of the backend to use. ``"gridmet"`` is the only supported source
        today and remains the default so callers do not have to specify it.
    freq:
        Temporal frequency string understood by :func:`pandas.date_range`.
        ``"MS"`` (monthly start) keeps notebook demos lightweight while still
        generating a datetime coordinate suitable for downstream analysis.
    chunks:
        Optional Dask-style mapping of dimension names to chunk sizes. When
        omitted, CubeDynamics falls back to the defaults defined by the
        ``load_gridmet_cube`` helper.
    **kwargs:
        Additional keyword arguments forwarded to :func:`load_gridmet_cube`.

    Returns
    -------
    xarray.DataArray
        Dask-backed DataArray with ``(time, y, x)`` dimensions for the requested
        variable.

    Examples
    --------
    >>> import cubedynamics as cd
    >>> boulder_aoi = {
    ...     "type": "Feature",
    ...     "properties": {"name": "Boulder, CO"},
    ...     "geometry": {
    ...         "type": "Polygon",
    ...         "coordinates": [[
    ...             [-105.35, 40.00],
    ...             [-105.35, 40.10],
    ...             [-105.20, 40.10],
    ...             [-105.20, 40.00],
    ...             [-105.35, 40.00],
    ...         ]],
    ...     },
    ... }
    >>> cube = cd.stream_gridmet_to_cube(
    ...     aoi_geojson=boulder_aoi,
    ...     variable="pr",
    ...     start="2000-01-01",
    ...     end="2020-12-31",
    ...     freq="MS",
    ...     chunks={"time": 120},
    ... )
    >>> cube
    <xarray.DataArray 'pr' ...>
    """

    if source != "gridmet":  # pragma: no cover - defensive branch
        raise ValueError(f"Unsupported gridMET source '{source}'.")

    prefer_streaming = kwargs.pop("prefer_streaming", True)
    if kwargs:
        unexpected = ", ".join(sorted(kwargs))
        raise TypeError(f"Unexpected keyword arguments: {unexpected}")

    bounds = _geojson_bounds(aoi_geojson)
    ds = load_gridmet_cube(
        variables=[variable],
        start=start,
        end=end,
        aoi=bounds,
        time_res=freq,
        chunks=chunks,
        prefer_streaming=prefer_streaming,
    )
    cube = ds[variable]
    cube.name = variable
    return cube


def _geojson_bounds(aoi_geojson: Mapping[str, Any]) -> Mapping[str, float]:
    """Convert a GeoJSON Feature/FeatureCollection into bounding-box dict."""

    if not isinstance(aoi_geojson, Mapping):
        raise TypeError("aoi_geojson must be a GeoJSON mapping")

    coords = _extract_coordinates(aoi_geojson)
    if not coords:
        raise ValueError("aoi_geojson does not contain any coordinates")

    lons = [pt[0] for pt in coords]
    lats = [pt[1] for pt in coords]
    return {
        "min_lon": min(lons),
        "max_lon": max(lons),
        "min_lat": min(lats),
        "max_lat": max(lats),
    }


def _extract_coordinates(obj: Mapping[str, Any] | Sequence[Any]) -> list[tuple[float, float]]:
    """Recursively extract lon/lat coordinate pairs from GeoJSON objects."""

    if isinstance(obj, Mapping):
        obj_type = obj.get("type")
        if obj_type == "FeatureCollection":
            coords: list[tuple[float, float]] = []
            for feature in obj.get("features", []):
                coords.extend(_extract_coordinates(feature))
            return coords
        if obj_type == "Feature":
            return _extract_coordinates(obj.get("geometry", {}))
        if "coordinates" in obj:
            return _extract_coordinates(obj["coordinates"])
        return []

    if isinstance(obj, Sequence) and obj and not isinstance(obj[0], (str, bytes)):
        if isinstance(obj[0], (int, float)) and len(obj) >= 2:
            lon = float(obj[0])
            lat = float(obj[1])
            return [(lon, lat)]
        coords: list[tuple[float, float]] = []
        for part in obj:
            coords.extend(_extract_coordinates(part))
        return coords

    return []


__all__ = ["stream_gridmet_to_cube"]
