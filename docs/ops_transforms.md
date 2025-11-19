# Transform verbs

**In plain English:**  
Transform verbs reshape or adjust cubes (filtering months, reprojecting, normalizing). They now run tile by tile when a VirtualCube streams large data, so you can apply the same transforms to decade-spanning cubes.

**What this page helps you do:**  
- Learn how transforms behave on streaming cubes
- See examples with VirtualCube inputs
- Know when to materialize for specialized needs

## Streaming-friendly transforms

Most transforms operate independently per tile, so the outputs combine cleanly.

```python
from cubedynamics import pipe, verbs as v

# Stream a tile-aware anomaly
streamed = pipe(cube) | v.anomaly(dim="time") | v.month_filter([6, 7, 8])
```

## Tips for large requests

- Keep transforms that require context (e.g., global normalization) aware of tile size; adjust `time_tile` if needed.
- Use `.debug_tiles()` on the source cube to see how many tiles will flow through the verbs.
- Add `v.peek()` or logging after key transforms when diagnosing unexpected values.

## Visualization after transforms

Plotting still streams:

```python
pipe(cube) | v.variance(dim="time") | v.plot_timeseries()
```

Large AOIs update as each tile finishes; reduce date spans to speed up.

---

## Legacy Technical Reference (kept for context)
# Operations – transform verbs

**In plain English:**  
Transform verbs reshape or filter a cube before you calculate statistics.
They are small, chainable steps that keep the cube structure intact.

**You will learn:**  
- What each transform verb does in plain language
- How to combine transforms in a short pipe
- Where to find the original technical reference

## What this is

These functions live in `cubedynamics.ops.transforms` and are re-exported as `cubedynamics.verbs`.
Each one returns a callable so you configure it once and feed it a cube through the `|` operator.

## Why it matters

Transforming cubes in-place keeps your workflow compact and reproducible.
You can center, filter, or subset data without losing metadata, which makes it easy to hand analyses to collaborators.

## How to use it

### `anomaly(dim)`
Calculates how far each value is from the mean along the chosen dimension.

```python
from cubedynamics import pipe, verbs as v

daily_anom = pipe(cube) | v.anomaly(dim="time")
```
This mean-centers the cube along `time` so values show departures from the average.

### `month_filter(months)`
Keeps only the month numbers you list, such as `[6, 7, 8]` for June–August.

```python
summer = pipe(cube) | v.month_filter([6, 7, 8])
```
This is a quick way to create seasonal subsets before running statistics.

You can combine transforms freely:

```python
pipe(cube) | v.anomaly(dim="time") | v.month_filter([6, 7, 8])
```
This first mean-centers the cube and then keeps only summer timesteps.

---

## Original Reference (kept for context)
# Operations Reference – Transforms

Transform verbs reshape or filter cubes before you compute downstream statistics. All functions live under `cubedynamics.ops.transforms` and are re-exported via `cubedynamics.verbs`. Examples assume `from cubedynamics import pipe, verbs as v` and a `cube` variable that is an `xarray` object.

## `anomaly(dim)`

Computes anomalies by subtracting the mean along a dimension.

```python
result = pipe(cube) | v.anomaly(dim="time")
```

- **Parameters**
  - `dim`: dimension name (e.g., `"time"`).
- **Returns**: `xarray.DataArray`/`Dataset` with mean-centered values.

## `month_filter(months)`

Filters a cube to the specified month numbers (1–12). Useful for seasonal composites before running statistics.

```python
result = pipe(cube) | v.month_filter([6, 7, 8]) | v.anomaly(dim="time")
```

- **Parameters**
  - `months`: iterable of integers representing desired months.
- **Behavior**: keeps the original metadata while dropping other timesteps.

Use these verbs as building blocks ahead of stats like variance or correlation.
