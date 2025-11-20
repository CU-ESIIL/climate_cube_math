import numpy as np
import xarray as xr

from cubedynamics.plotting.cube_plot import CubePlot, ScaleFillContinuous


def test_facet_wrap_generates_panels(tmp_path):
    data = xr.DataArray(
        np.arange(2 * 3 * 2 * 2).reshape(2, 3, 2, 2),
        dims=("scenario", "time", "y", "x"),
        coords={"scenario": ["A", "B"]},
        name="facet_demo",
    )

    plot = CubePlot(data, show_progress=False, out_html=str(tmp_path / "facet.html"))
    plot.facet_wrap("scenario", ncol=2)
    html = plot.to_html()

    assert html.count("cube-facet-panel") >= 2
    assert "scenario = A" in html
    assert "scenario = B" in html


def test_cubeplot_save_html(tmp_path):
    data = xr.DataArray(
        np.arange(8).reshape(2, 2, 2), dims=("time", "y", "x"), name="demo"
    )

    plot = CubePlot(data, show_progress=False, out_html=str(tmp_path / "save.html"))
    target = tmp_path / "figure.html"
    plot.save(target)

    assert target.exists()
    contents = target.read_text()
    assert "cube-figure" in contents
    assert "cube-caption" in contents or "cube-viewer" in contents


def test_scale_fill_continuous_diverging_limits():
    data = xr.DataArray(
        np.array(
            [
                [[-2.0, -1.0], [0.0, 1.0]],
            ]
        ),
        dims=("time", "y", "x"),
        name="temperature_anomaly",
    )
    scale = ScaleFillContinuous(center=0.0, palette="diverging")
    limits = scale.infer_limits(data)

    assert limits[0] == -limits[1]
    assert scale.resolved_cmap() != ""

    plot = CubePlot(data, fill_scale=scale, show_progress=False)
    html = plot.to_html()
    assert "cube-figure" in html
    assert "colorbar" in html or "cube-viewer" in html


def test_facet_grid_labels(tmp_path):
    data = xr.DataArray(
        np.arange(2 * 2 * 2 * 2 * 2).reshape(2, 2, 2, 2, 2),
        dims=("time", "scenario", "region", "y", "x"),
        coords={"scenario": ["A", "B"], "region": ["R1", "R2"]},
        name="grid_demo",
    )
    plot = CubePlot(data, show_progress=False, out_html=str(tmp_path / "grid.html"))
    plot.facet_grid(row="scenario", col="region")
    html = plot.to_html()

    assert "scenario = A" in html
    assert "region = R1" in html
    assert html.count("cube-facet-panel") >= 4
