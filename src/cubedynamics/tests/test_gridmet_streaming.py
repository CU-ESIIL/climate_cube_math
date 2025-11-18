"""Tests for the gridMET streaming helper."""

import cubedynamics as cd


def test_stream_gridmet_to_cube_default_source_smoke():
    """Calling the helper without `source` should return a time-indexed cube."""

    boulder_aoi = {
        "type": "Feature",
        "properties": {"name": "Boulder, CO"},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-105.35, 40.00],
                [-105.35, 40.01],
                [-105.34, 40.01],
                [-105.34, 40.00],
                [-105.35, 40.00],
            ]],
        },
    }

    cube = cd.stream_gridmet_to_cube(
        aoi_geojson=boulder_aoi,
        variable="pr",
        start="2000-01-01",
        end="2000-12-31",
        freq="MS",
        chunks={"time": 12},
    )

    assert "time" in cube.dims
    assert cube.name == "pr"
