## Quickstart: A 10-Minute Tour of CubeDynamics

This short tour shows how to load a small environmental data cube, run a few common analyses, and explore the results interactively.  
CubeDynamics treats gridded climate and remote-sensing datasets as **spatiotemporal cubes**:

```
V(lat, lon, time)
```

This structure lets us express environmental questions directly in code—without manually handling rasters, stacks, or time indices.

---

## 1. Install

```bash
pip install cubedynamics
```

---

## 2. Load a small NDVI cube

Here we load a one-year NDVI cube for a small region near Boulder, Colorado.  
CubeDynamics automatically retrieves data, aligns metadata, and constructs a coherent `time × y × x` cube.

```python
import cubedynamics as cd
from cubedynamics import pipe, verbs as v

ndvi = cd.ndvi(
    lat=40.0,
    lon=-105.25,
    start="2020-01-01",
    end="2020-12-31",
)
ndvi
```

You now have a fully functional data cube that preserves both **space** and **time**.

---

## 3. Compute a climatology and anomaly

Cube-based analysis allows transformations that depend on the full spatiotemporal context.

```python
ndvi_clim = pipe(ndvi) | v.climatology()
ndvi_anom = pipe(ndvi, ndvi_clim) | v.anomaly()
```

`v.climatology()` computes a baseline seasonal cycle.  
`v.anomaly()` shows deviations from that seasonal expectation.

These are operations that traditionally require many raster manipulations—here they are expressed directly on the cube.

---

## 4. Explore the result in the 3D cube viewer

```python
pipe(ndvi_anom) | v.plot()
```

The interactive cube viewer displays:

- **Temporal slices** through the back face,  
- **Spatial slices** across the sides,  
- **Dynamic rotation and zoom** for exploring patterns.

This makes it easy to see when and where NDVI departs from typical seasonal behavior.

---

## 5. Make a simple map

Many analyses only need a 2-D spatial snapshot (e.g., a seasonal mean or anomaly).  
You can visualize these with:

```python
pipe(ndvi_anom) | v.map()
```

This produces a lightweight map view with consistent colormaps and metadata.

---

## 6. What next?

Now that you have a working cube and basic transformations, explore:

- **Conceptcepts**
  - What is a cube?  
  - Pipe & verb grammar  
  - VirtualCubes and streaming  

- **How-to Guides**  
  - NDVI anomalies  
  - Climate variance  
  - Correlation cubes  

- **Visualization**  
  - Cube viewer (`v.plot`)  
  - Map viewer (`v.map`)  

- **API Reference**  

CubeDynamics provides a unified, cube-native way to work with spatiotemporal environmental data—simple enough for quick exploration, powerful enough for large-scale scientific analysis.
