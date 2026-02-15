# SUMO EV Charging & Battery Simulation

This repository contains scripts and input files to run SUMO-based electric vehicle (EV) simulations, analyze low-battery events, and generate charging-station placements for a road network.

The project was developed to support experiments with EV routing, battery drain tracking, and charger placement. It includes helper scripts to create a SUMO config, generate charging-station add files from geographic coordinates, and collect vehicles that reach low battery during a simulation.

---

## Quick summary

- Use `create_sumo_config.py` to generate a SUMO configuration (`.sumo.cfg`) combining a network, routes and additional files.
- Use `place_chargers.py` to turn a list of lon/lat charger positions into a SUMO `*.add.xml` (nearest-lane placement).
- Run SUMO (or `sumo-gui`) with the generated config to simulate vehicle routes and battery usage.
- Use `app.py` to record vehicles whose battery percentage falls below a threshold (writes a CSV of low-battery vehicle positions).

---

## Files of interest

- **Network & routes**
  - `2345net.net.xml` — SUMO network in this folder.
  - `routes_electric_1500.rou.xml`, `routes_electric_final.rou.xml`, etc. — route files used for EV traffic.

- **Helper scripts**
  - `create_sumo_config.py` — builds `simulation_with_charging.sumo.cfg` from `net`, `route`, and `additional` files.
  - `place_chargers.py` — places chargers (lon/lat list) onto the network and writes `chargingStations_generated.add.xml`.
  - `app.py` — connects to SUMO via TraCI and records vehicles with battery < 10% into `discharged_battries_optimized.csv` (see notes below).
  - `sumocoordinates.py`, `largerPOI.py`, `batterylevelVStime.py` — additional utilities used in data processing or coordinate tasks.

- **Charging / battery add-ons and outputs**
  - `battery_devices_1500_final1.add.xml`, `battery_devices.add.xml`, ... — battery/device definitions for vehicles.
  - `chargingStations_location.xml`, `chargingStations_generated.add.xml` — charger definitions and locations.
  - `Discharged_EVs.xml`, `battery_output.xml`, `battery_output_final.xml` — example outputs produced by SUMO or scripts.

- **Configurations**
  - `simulation_with_charging.sumo.cfg` — (generated) convenience SUMO config combining network, routes and additional files.
  - `configuration.sumo.cfg`, `config_optimized.sumo.cfg` — other configuration variants present in repo.

- **Data & logs**
  - CSVs: `final_battery_positions.csv`, `low_battery_positions.csv`, `battery_levels_over_time.csv`, `discharged_battries_unoptimized.csv`, etc.

---

## Requirements / Prerequisites

- SUMO (recommended latest stable release) installed and on your PATH. `sumo` and `sumo-gui` must be callable.
- Python 3.8+.
- Common Python packages used by scripts (install via pip):

```bash
pip install sumolib traci pandas lxml
```

Notes:
- `sumolib` and `traci` are part of the SUMO Python tools. If you installed SUMO via a package that includes the Python bindings, you may already have them.
- Some scripts use only standard library modules (xml, csv, math) and will work without extra packages.

---

## Typical workflow / usage

1. Inspect and prepare the input files (network, route files, charging station coordinates, battery devices).

2. (Optional) Generate a SUMO config that bundles inputs:

```bash
python create_sumo_config.py
# Produces: simulation_with_charging.sumo.cfg
```

3. (Optional) Generate charging station add file from lon/lat points:

```bash
python place_chargers.py
# Produces: chargingStations_generated.add.xml
# Add this file to your config's additional-files if desired
```

4. Run SUMO (or SUMO GUI) using the chosen configuration. Example (GUI):

```bash
sumo-gui -c simulation_with_charging.sumo.cfg
# or, for headless:
# sumo -c simulation_with_charging.sumo.cfg
```

5. Run `app.py` to connect to SUMO via TraCI and record vehicles that drop below the low-battery threshold.

```bash
python app.py
# Output: discharged_battries_optimized.csv (list of low-battery vehicles with positions)
```

---

## Notes & important details discovered in the code

- `app.py` uses `sumolib.checkBinary('sumo-gui')` and starts SUMO using a configuration named `configuration_optmized.sumo.cfg`. There are a few similarly named cfg files in this repository (e.g. `config_optimized.sumo.cfg`, `configuration.sumo.cfg`, `simulation_with_charging.sumo.cfg`). Verify the filename in `app.py` matches a config file in this repo or edit `app.py` to point to the correct config.

- `app.py` extracts per-vehicle parameters `device.battery.actualBatteryCapacity` and `device.battery.maximumBatteryCapacity` via TraCI. This requires that vehicles in your route/additional files have those attributes (see `battery_devices_*.add.xml`). If your vehicles don't expose those parameters, adapt the vehicle/device definitions accordingly.

- `place_chargers.py` assumes the network uses lon/lat coordinates. If your network uses projected coordinates, you must convert lon/lat to the net's coordinate system or adapt the helper function `to_net_xy`.

---

## Outputs

- `discharged_battries_optimized.csv` (written by `app.py`) — CSV containing `vehicle_id`, `battery_percentage`, `longitude`, `latitude` for vehicles recorded below threshold.
- `Discharged_EVs.xml` — example battery output produced by SUMO when configured via `create_sumo_config.py`.
- `chargingStations_generated.add.xml` — generated by `place_chargers.py` when executed.

---

## Extending the project

- Adjust battery thresholds and parameters in `app.py` for other battery-percentage cutoffs (currently uses < 10%).
- Improve `place_chargers.py` by reading charger points from a CSV or GeoJSON to avoid hard-coded lists.
- Add a small wrapper CLI to chain config creation, charger placement, and simulation runs with a single command.
- Add tests or a minimal example to reproduce results quickly.

---

## Troubleshooting

- TraCI errors: ensure SUMO and its Python bindings (`traci`) are correctly installed and that the SUMO binary is found by `sumolib.checkBinary()`.
- Mismatched coordinate systems: if charger placement yields warnings about "no lane found", the network likely uses projected (non-lon/lat) coordinates.
- Typo in config filename: if `app.py` fails to start SUMO, check the config filename inside `app.py` (`configuration_optmized.sumo.cfg`) and rename or update it to an existing config (e.g. `config_optimized.sumo.cfg` or `simulation_with_charging.sumo.cfg`).

---

## Contributing

Contributions are welcome. Suggested workflow:

- Create an issue describing the desired feature or bug.
- Send a pull request with focused changes and a short description of behavior.

---

## License & attribution

Add your preferred license here (for example, MIT). If you want, I can add a `LICENSE` file.

---

## Contact

If you want me to further: run the simulations, fix the `app.py` config filename, or add a CLI wrapper, tell me which step to do next.

