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

- **Parameters**: pass any Lexcube keyword arguments (`title`, `cmap`, `vmin`, `vmax`).
- **Notes**: Widgets render only in live notebook environments.

### `v.plot_median_over_space(ylabel=None, title=None)`

Generate QA plots summarizing the spatial median over time.

```python
from cubedynamics import pipe, verbs as v

ax = (
    pipe(cube)
    | v.plot_median_over_space(
        ylabel="Median NDVI z-score",
        title="Median NDVI z-score over time",
    )
)
```

- **Returns**: Matplotlib axis for further customization.
- **Notes**: Useful for spot-checking anomalies before exporting results.

### `v.quick_map()` (planned)

Future work will expose small multiples and static PNG exporters for dashboards. Track development in the [Roadmap](../dev/roadmap.md).
