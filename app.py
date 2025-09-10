import traci
import sumolib
import csv

# Define output CSV file
output_file = "last_battery_positions.csv"

# Start SUMO
sumoBinary = sumolib.checkBinary('sumo-gui')  # or 'sumo' for no GUI
sumoCmd = [sumoBinary, "-c", "configuration.sumo.cfg", "--start"]
traci.start(sumoCmd)

low_battery_vehicles = []

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    for veh_id in traci.vehicle.getIDList():
        try:
            actual = float(traci.vehicle.getParameter(veh_id, "device.battery.actualBatteryCapacity"))
            maximum = float(traci.vehicle.getParameter(veh_id, "device.battery.maximumBatteryCapacity"))

            if maximum > 0:
                percentage = (actual / maximum) * 100
            else:
                percentage = 0

            if percentage <= 10:  # Battery lower than 10%
                x, y = traci.vehicle.getPosition(veh_id)

                print(f"⚡ Vehicle {veh_id} | Battery: {percentage:.2f}% | Position: ({x:.2f}, {y:.2f})")

                low_battery_vehicles.append({
                    "vehicle_id": veh_id,
                    "battery_percentage": percentage,
                    "x_position": x,
                    "y_position": y
                })

        except traci.TraCIException:
            pass  # ignore vehicles without battery

traci.close()

# Save to CSV
with open(output_file, mode="w", newline="") as csv_file:
    fieldnames = ["vehicle_id", "battery_percentage", "x_position", "y_position"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for entry in low_battery_vehicles:
        writer.writerow(entry)

print(f"\n✅ Low battery vehicle positions saved to: {output_file}")