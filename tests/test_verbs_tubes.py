import numpy as np
import xarray as xr

from cubedynamics import pipe, verbs as v


def _tiny_cube(seed: int = 0):
    rng = np.random.default_rng(seed)
    time = np.arange("2000-01", "2000-06", dtype="datetime64[M]")
    y = np.linspace(0, 3, 4)
    x = np.linspace(0, 3, 4)
    data = rng.random((len(time), len(y), len(x)), dtype=np.float32)
    return xr.DataArray(
        data,
        dims=("time", "y", "x"),
        coords={"time": time, "y": y, "x": x},
        name="demo_cube",
    )


def test_tubes_verb_smoke_default():
    cube = _tiny_cube()
    viewer = pipe(cube) | v.tubes()
    assert viewer is not None


def test_tubes_verb_select_explicit_id():
    cube = _tiny_cube(seed=1)
    viewer = pipe(cube) | v.tubes(select="longest")
    assert viewer is not None
