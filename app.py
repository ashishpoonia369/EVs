import traci
import sumolib
import csv

output_file = "discharged_battries_optimized.csv"

sumoBinary = sumolib.checkBinary('sumo-gui')
sumoCmd = [sumoBinary, "-c", "configuration_optmized.sumo.cfg", "--start"]
traci.start(sumoCmd)

low_battery_vehicles = []
recorded_vehicles = set()

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    for veh_id in traci.vehicle.getIDList():
        try:
            actual = float(traci.vehicle.getParameter(
                veh_id, "device.battery.actualBatteryCapacity"))
            maximum = float(traci.vehicle.getParameter(
                veh_id, "device.battery.maximumBatteryCapacity"))

            percentage = (actual / maximum) * 100 if maximum > 0 else 0

            if percentage < 10 and veh_id not in recorded_vehicles:
                x, y = traci.vehicle.getPosition(veh_id)

                # 🔥 Convert to latitude/longitude
                lon, lat = traci.simulation.convertGeo(x, y)

                print(f"⚡ Vehicle {veh_id} | Battery: {percentage:.2f}% | LatLon: ({lat:.6f}, {lon:.6f})")

                low_battery_vehicles.append({
                    "vehicle_id": veh_id,
                    "battery_percentage": percentage,
                    "longitude": lon,
                    "latitude": lat
                })
                recorded_vehicles.add(veh_id)

        except traci.TraCIException:
            pass

traci.close()

with open(output_file, mode="w", newline="") as csv_file:
    fieldnames = ["vehicle_id", "battery_percentage", "longitude", "latitude"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(low_battery_vehicles)

print(f"\n✅ Saved: {output_file}")