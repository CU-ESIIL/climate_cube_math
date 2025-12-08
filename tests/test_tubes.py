import numpy as np
import xarray as xr

from cubedynamics.tubes import (
    compute_suitability_from_ndvi,
    label_tubes,
    compute_tube_metrics,
    tube_to_vase_definition,
)
from cubedynamics.vase import VaseDefinition, VaseSection


def test_compute_suitability_from_ndvi_dims_and_dtype():
    ndvi = xr.DataArray(
        np.linspace(0, 1, num=5 * 4 * 4).reshape(5, 4, 4),
        dims=("time", "y", "x"),
        coords={"time": np.arange(5), "y": np.arange(4), "x": np.arange(4)},
    )

    mask = compute_suitability_from_ndvi(ndvi, lo=0.2, hi=0.7)

    assert mask.dims == ndvi.dims
    assert mask.dtype == bool
    assert mask.name == "ndvi_suitability"


def test_label_tubes_simple_components():
    mask = xr.DataArray(
        data=np.array(
            [
                [[True, False, False], [False, False, False], [False, False, True]],
                [[False, False, False], [False, True, False], [False, False, False]],
            ]
        ),
        dims=("time", "y", "x"),
        coords={"time": [0, 1], "y": [0, 1, 2], "x": [0, 1, 2]},
    )

    labeled = label_tubes(mask)

    assert labeled.dims == mask.dims
    assert labeled.attrs["tube_count"] == 3
    assert int(labeled.max()) >= 1


def test_compute_tube_metrics_columns_and_counts():
    tube_ids = xr.DataArray(
        data=np.array(
            [
                [[1, 0], [0, 0]],
                [[1, 1], [0, 0]],
                [[0, 2], [2, 0]],
            ]
        ),
        dims=("time", "y", "x"),
        coords={"time": [0, 1, 2], "y": [0, 1], "x": [0, 1]},
    )

    metrics = compute_tube_metrics(tube_ids)

    expected_columns = {
        "tube_id",
        "duration_steps",
        "n_voxels",
        "time_start",
        "time_end",
        "y_min",
        "y_max",
        "x_min",
        "x_max",
        "cells_per_timestep_mean",
        "cells_per_timestep_max",
    }

    assert expected_columns.issubset(set(metrics.columns))
    assert set(metrics["tube_id"].unique()) == {1, 2}
    assert metrics.loc[metrics["tube_id"] == 1, "duration_steps"].iloc[0] == 2


def test_tube_to_vase_definition_creates_sections():
    tube = xr.DataArray(
        data=np.array(
            [
                [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
                [[0, 0, 0], [1, 1, 0], [0, 0, 0]],
                [[0, 0, 1], [0, 1, 0], [0, 0, 0]],
            ]
        ),
        dims=("time", "y", "x"),
        coords={"time": [0, 1, 2], "y": [0.0, 1.0, 2.0], "x": [0.0, 1.0, 2.0]},
    )

    cube = xr.DataArray(
        np.zeros_like(tube), dims=tube.dims, coords=tube.coords
    )

    vase = tube_to_vase_definition(cube, tube, tube_id=1)

    assert isinstance(vase, VaseDefinition)
    assert len(vase.sections) >= 1
    assert all(isinstance(sec, VaseSection) for sec in vase.sections)
    assert all(sec.polygon.is_valid for sec in vase.sections)
    assert {sec.time for sec in vase.sections} == {0, 1, 2}
