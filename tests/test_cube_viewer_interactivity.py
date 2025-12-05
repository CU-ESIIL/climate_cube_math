import numpy as np
import pandas as pd
import xarray as xr

from cubedynamics.plotting.cube_viewer import cube_from_dataarray


def test_cube_viewer_emits_interactive_markup(tmp_path):
    data = xr.DataArray(
        np.arange(4 * 8 * 8, dtype=float).reshape(4, 8, 8),
        dims=("time", "y", "x"),
        coords={
            "time": pd.date_range("2023-01-01", periods=4, freq="D"),
            "y": np.arange(8),
            "x": np.arange(8),
        },
        name="demo",
    )

    html = cube_from_dataarray(
        data,
        out_html=str(tmp_path / "viewer.html"),
        return_html=True,
        show_progress=False,
        thin_time_factor=1,
        debug=True,
        fig_id="interact-test",
    )

    assert 'id="cube-figure-interact-test"' in html
    assert 'id="cube-drag-interact-test"' in html
    assert 'data-debug="1"' in html
    assert 'addEventListener("pointerdown"' in html
    assert 'addEventListener("mousedown"' in html
    assert 'addEventListener("touchstart"' in html
    assert 'addEventListener("wheel"' in html
    assert 'const figureId = "cube-figure-interact-test"' in html
    assert (tmp_path / "viewer.html").exists()
