import os
import traci
import sumolib
import csv
from collections import defaultdict

print("Current working directory:", os.getcwd())

# Define output files
position_csv = "low_battery_positions.csv"
battery_time_csv = "battery_levels_over_time.csv"

# Start SUMO
sumoBinary = sumolib.checkBinary('sumo-gui')
sumoCmd = [sumoBinary, "-c", "configuration.sumo.cfg", "--start"]
traci.start(sumoCmd)

# Data storage
low_battery_positions = []
battery_history = defaultdict(list)  # {veh_id: [(time, percentage), ...]}

while traci.simulation.getMinExpectedNumber() > 0:
    current_time = traci.simulation.getTime()
    traci.simulationStep()

    for veh_id in traci.vehicle.getIDList():
        try:
            actual = float(traci.vehicle.getParameter(veh_id, "device.battery.actualBatteryCapacity"))
            maximum = float(traci.vehicle.getParameter(veh_id, "device.battery.maximumBatteryCapacity"))
            
            if maximum > 0:
                percentage = (actual / maximum) * 100
            else:
                percentage = 0

            # Record all battery levels over time
            battery_history[veh_id].append((current_time, percentage))

            # Check for 10% threshold (position recording)
            if percentage == 10:
                x, y = traci.vehicle.getPosition(veh_id)
                low_battery_positions.append({
                    "vehicle_id": veh_id,
                    "battery_percentage": percentage,
                    "x_position": x,
                    "y_position": y
                })

        except traci.TraCIException:
            pass

traci.close()

# Save position data
with open(position_csv, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["vehicle_id", "battery_percentage", "x_position", "y_position"])
    writer.writeheader()
    writer.writerows(low_battery_positions)

# Save battery time-series data
with open(battery_time_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["vehicle_id", "time", "battery_percentage"])
    for veh_id, readings in battery_history.items():
        for time, percentage in readings:
            writer.writerow([veh_id, time, percentage])

print(f"\n✅ Position data saved to: {position_csv}")
print(f"✅ Battery time-series data saved to: {battery_time_csv}")