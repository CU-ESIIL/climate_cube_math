# Visualization verbs

Visualization verbs display cubes inline or generate QA plots without leaving the pipe chain.

<a id="vshow_cube_lexcube"></a>

### `v.show_cube_lexcube(**kwargs)`

Integrate [Lexcube](https://github.com/carbonplan/lexcube) for interactive `(time, y, x)` exploration. The verb displays the widget as a side effect and returns the original cube so pipelines keep flowing.

```python
from cubedynamics import pipe, verbs as v

pipe(cube) \
    | v.month_filter([6, 7, 8]) \
    | v.show_cube_lexcube(title="PRISM JJA precipitation", cmap="RdBu_r")
```

- **Parameters**: pass any Lexcube keyword arguments (`title`, `cmap`, `vmin`, `vmax`). Datasets with a single data variable are automatically converted to a DataArray.
- **Notes**: Widgets render only in live notebook environments and require a 3D `(time, y, x)` cube. Reducers such as `v.mean`/`v.variance` should use `keep_dim=True` to preserve this layout.

For QA plots outside Lexcube, call the functional helper `cubedynamics.plot_median_over_space(cube, ...)`.

### `v.quick_map()` (planned)

Future work will expose small multiples and static PNG exporters for dashboards. Track development in the [Roadmap](../dev/roadmap.md).
