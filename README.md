# SUMO EV Charging & Battery Simulation

This repository contains scripts and input files to run SUMO-based electric vehicle (EV) simulations, analyze low-battery events, and generate charging-station placements for a road network.

The project supports experiments with EV routing, battery drain tracking, charger placement, and post-simulation analysis. The included scripts help you create SUMO configuration files, place chargers from geographic coordinates, run/scrape TraCI outputs, and produce visualizations for comparing scenarios.

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

## Results (figures)

The repository includes visual outputs in the `images/` folder. Below are the main figures and short captions; open the images for full detail.

- Discharge — Optimized scenario:

![Discharge — Optimized](images/Discharge_optimized.png)

- Discharge — Unoptimized scenario:

![Discharge — Unoptimized](images/Discharge_unoptimized.png)

- Cluster of low-battery points — Optimized:

![Cluster — Optimized](images/clustter_optimized.png)

- Cluster of low-battery points — Unoptimized:

![Cluster — Unoptimized](images/Clustter_unoptimized.png)

- Cluster load comparison — Optimized:

![Cluster load — Optimized](images/clustter_load_optimized.png)

- Cluster load comparison — Unoptimized:

![Cluster load — Unoptimized](images/clustter_load_unoptimized.png)

- Traffic Analysis Zones (TAZ) / landuse used in spatial analysis:

![TAZ / Landuse](images/TAZes.png)

- High-resolution landuse raster used for planning (GeoTIFF):

`images/landuse_surat_modified.tif`

---

## Files of interest

- **Network & routes**
  - `2345net.net.xml` — SUMO network in this folder.
  - Route files: any `routes_*.rou.xml` files in the repo.

- **Helper scripts**
  - `create_sumo_config.py` — builds `simulation_with_charging.sumo.cfg` from `net`, `route`, and `additional` files.
  - `place_chargers.py` — places chargers (lon/lat list) onto the network and writes `chargingStations_generated.add.xml`.
  - `app.py` — connects to SUMO via TraCI and records vehicles with battery < 10% into `discharged_battries_optimized.csv`.

- **Add/Output files**
  - `battery_devices_*.add.xml` — battery/device definitions for vehicles.
  - `chargingStations_generated.add.xml`, `chargingStations_location.xml` — charger definition files.
  - `Discharged_EVs.xml`, `battery_output*.xml` — example outputs from SUMO.

---

## Requirements / Prerequisites

- SUMO (latest stable recommended) installed and on your PATH (`sumo` and `sumo-gui` accessible).
- Python 3.8+.
- Python packages (example):

```bash
pip install sumolib traci pandas lxml
```

---

## Typical workflow / usage

1. Prepare or edit input files: network (`*.net.xml`), routes (`*.rou.xml`), device/add files.
2. (Optional) Generate a config:

```bash
python create_sumo_config.py
```

3. (Optional) Generate charging stations from lon/lat:

```bash
python place_chargers.py
```

4. Run SUMO with the config:

```bash
sumo-gui -c simulation_with_charging.sumo.cfg
# or headless:
# sumo -c simulation_with_charging.sumo.cfg
```

5. Run `app.py` to record low-battery vehicles via TraCI:

```bash
python app.py
```

Output CSVs and PNGs will be written to the repository (see `images/` and `*.csv`).

---

## Notes & troubleshooting

- `app.py` expects the vehicle/device definitions to expose `device.battery.actualBatteryCapacity` and `device.battery.maximumBatteryCapacity` via TraCI.
- `place_chargers.py` assumes the network uses lon/lat; convert coordinates if your net uses projected coords.
- If `app.py` fails to start SUMO, verify the config filename inside `app.py` and ensure the file exists.

---

## Next steps I can do for you

- Update `app.py` to point to `simulation_with_charging.sumo.cfg` (or another config you pick).
- Add a `requirements.txt` and a small CLI script to run the full pipeline.
- Produce a short notebook that loads `discharged_battries_optimized.csv` and renders the figures shown in `images/`.

If you want any of these, tell me which to do next.
