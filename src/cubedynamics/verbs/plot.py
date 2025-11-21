"""Plotting verb for displaying cubes via :class:`CubePlot`."""

from __future__ import annotations

from dataclasses import dataclass

import xarray as xr

from ..piping import Verb
from ..plotting import CubePlot
from ..vase import extract_vase_from_attrs

__all__ = ["plot"]


@dataclass
class PlotOptions:
    title: str | None = None
    cmap: str = "viridis"
    thin_time_factor: int = 4


def plot(
    title: str | None = None,
    cmap: str = "viridis",
    thin_time_factor: int = 4,
) -> Verb:
    """High-level cube viewer.

    - Uses :class:`~cubedynamics.plotting.CubePlot` under the hood
    - Draws the cube via :meth:`~cubedynamics.plotting.cube_plot.CubePlot.geom_cube`
    - If a vase is attached in ``attrs['vase']``, overlays it via
      ``.stat_vase(...).geom_vase_outline()``
    - Applies ``theme_cube_studio`` with tight axis labels.
    """

    opts = PlotOptions(title=title, cmap=cmap, thin_time_factor=thin_time_factor)

    def _plot(da: xr.DataArray):
        plot_title = opts.title or getattr(da, "name", None)

        # 1. Build CubePlot for this cube
        p = CubePlot(da, title=plot_title, cmap=opts.cmap, thin_time_factor=opts.thin_time_factor)

        # 2. Draw cube
        p = p.geom_cube(cmap=opts.cmap)

        # 3. If a vase is present, overlay outline
        vase = extract_vase_from_attrs(da)
        if vase is not None:
            p = p.stat_vase(vase).geom_vase_outline(
                color="limegreen",
                alpha=0.6,
            )

        # 4. Apply studio theme with tight axes (implementation in CubePlot)
        p = p.theme_cube_studio(tight_axes=True)

        # NOTE: Do NOT call display() here.
        # Returning the CubePlot object lets Jupyter render it once.
        return p

    return Verb(_plot)
