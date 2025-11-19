# NDVI z-scores

## What is NDVI?

The **Normalized Difference Vegetation Index (NDVI)** measures vegetation
vigour by contrasting the high reflectance of healthy plants in the near
infrared (NIR) with their low reflectance in the red band:

\[
NDVI = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}
\]

Values range from -1 to 1. Dense, photosynthetically active vegetation
produces high NDVI, while bare soil, snow, or water produce lower values.

## Why standardize NDVI?

Each pixel experiences its own seasonal cycle and lighting geometry. To detect
unusual conditions (drought, disturbance, phenology shifts) we standardize each
pixel relative to its own history. This is done with a **z-score** over time:

\[
z = \frac{x_t - \mu_{pixel}}{\sigma_{pixel}}
\]

where \(\mu_{pixel}\) and \(\sigma_{pixel}\) are the pixel's mean and
standard deviation across the available time series. The resulting NDVI
z-score cube highlights anomalies rather than absolute greenness.

## Mapping to `cubedynamics`

The package provides two key helpers exposed via the verbs namespace:

- `cubedynamics.verbs.ndvi_from_s2` turns Sentinel-2 Level-2A surface
  reflectance cubes into NDVI cubes.
- `cubedynamics.verbs.zscore` standardizes each pixel along the time
  dimension (or any other axis you select).

Together they produce the NDVI z-score cubes that downstream statistics and
visualizations consume.

## End-to-end example

```python
import cubedynamics as cd
from cubedynamics import pipe, verbs as v

s2 = cd.load_sentinel2_cube(
    lat=43.89,
    lon=-102.18,
    start="2023-06-01",
    end="2023-06-30",
    edge_size=256,
)

ndvi_z = (
    pipe(s2)
    | v.ndvi_from_s2()
    | v.zscore(dim="time")
)
```
