# SUMO EV Charging & Battery Simulation

This project focuses on modelling and optimizing Electric Vehicle (EV) charging infrastructure for Surat city using microscopic traffic simulation. The workflow integrates transportation demand modelling, GIS analysis, clustering algorithms, and SUMO-based EV simulations to identify optimal charging station locations.

The main objective is to:

- Analyze EV travel demand using Origin–Destination (OD) matrices.
- Simulate EV battery behaviour in realistic traffic conditions.
- Identify locations where EV batteries frequently drop below critical levels.
- Apply clustering techniques to determine optimal charging station placement.
- Validate charging infrastructure effectiveness through simulation.

---

## Quick summary

- Use `create_sumo_config.py` to build a SUMO configuration file combining a network, routes, and additional files.
- Use `place_chargers.py` to convert lon/lat charger points into a SUMO `*.add.xml` file (nearest-lane placement).
- Use SUMO (GUI or headless) to run the simulation and `app.py` (TraCI) to record vehicles that drop below a battery threshold.

---

## Core concept

This project demonstrates a reproducible workflow to study where and why electric vehicles run low on battery, and how charger placement changes outcomes. The core ideas:

- Simulate EV trips on a realistic road network with SUMO and route files.
- Model battery state for vehicles using SUMO's device/battery extensions (via `*.add.xml` files).
- Place charging stations on lanes (automatically or manually) and include them in the simulation configuration.
- Detect low-battery events either from SUMO outputs or in real time with TraCI (see `app.py`).
- Produce visual and numerical summaries (CSV and PNG outputs) to compare scenarios such as optimized vs unoptimized charger placement.

This setup supports iterative experiments: change routes, adjust charger locations, re-run simulations, and compare discharge/clustering metrics.

---

## Study Area
The study focuses on Surat city, India
Inputs include:
  - Land-use dattaser
  - TAZ boundaries
  - Population and employement data
  - Road network converter to SUMO formate
### Example TAZ visualization:

  - Traffic Analysis Zones (TAZ) / landuse used in spatial analysis:
  ![TAZ / Landuse](Images/TAZes.png)

- High-resolution landuse raster used for planning (GeoTIFF):

`Images/landuse_surat_modified.tif`

- Discharge — Optimized scenario:

![Discharge — Optimized](Images/Discharge_optimized.png)

- Discharge — Unoptimized scenario:

![Discharge — Unoptimized](Images/Discharge_unoptimized.png)

- Cluster of low-battery points — Optimized:

![Cluster — Optimized](Images/clustter_optimized.png)

- Cluster of low-battery points — Unoptimized:

![Cluster — Unoptimized](Images/Clustter_unoptimized.png)

- Cluster load comparison — Optimized:

![Cluster load — Optimized](Images/clustter_load_optimized.png)

- Cluster load comparison — Unoptimized:

![Cluster load — Unoptimized](Images/clustter_load_unoptimized.png)




---

## Tools & Technologies

- SUMO (Simulation of Urban Mobility)
- Python
- TraCI API
- GeoPandas
- QGIS

---


## Key Insights

- Charging demand clusters align with dense travel corridors.
- Optimized station placement reduces battery depletion risk.
- Spatial clustering improves infrastructure efficiency.

---
