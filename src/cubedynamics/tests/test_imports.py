"""Basic import smoke tests for the cubedynamics package."""

import pytest

import cubedynamics


def test_version_exposed():
    """Ensure the package exposes a version string."""
    assert isinstance(cubedynamics.__version__, str)


def test_streaming_helpers_are_callable():
    """All public streaming helpers should be importable."""
    public_funcs = [
        cubedynamics.stream_gridmet_to_cube,
        cubedynamics.stream_prism_to_cube,
        cubedynamics.correlation_cube,
    ]
    for func in public_funcs:
        assert callable(func)


def test_streaming_stubs_raise_not_implemented():
    """Only the unimplemented helpers should raise NotImplementedError."""
    stub_funcs = [
        cubedynamics.stream_prism_to_cube,
        cubedynamics.correlation_cube,
    ]
    for func in stub_funcs:
        with pytest.raises(NotImplementedError):
            if func is cubedynamics.correlation_cube:
                func(None, [None])
            else:
                func(None)
