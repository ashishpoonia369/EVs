import xml.etree.ElementTree as ET

# -------------------------------
# Input files
# -------------------------------
net_file = "2345net.net.xml"
route_file = "routes_electric_1500.rou.xml"
battery_file = "battery_devices_1500_final1.add.xml"
charging_file = "chargingStations_location.xml"

# Output config name
output_config = "simulation_with_charging.sumo.cfg"

# -------------------------------
# Create XML structure
# -------------------------------
configuration = ET.Element("configuration")

# INPUT SECTION
input_tag = ET.SubElement(configuration, "input")

ET.SubElement(input_tag, "net-file", value=net_file)
ET.SubElement(input_tag, "route-files", value=route_file)

# Multiple additional files separated by space
ET.SubElement(
    input_tag,
    "additional-files",
    value=f"{battery_file} {charging_file}"
)

# OUTPUT SECTION (optional)
output_tag = ET.SubElement(configuration, "output")
ET.SubElement(output_tag, "battery-output", value="Discharged_EVs.xml")

# -------------------------------
# Write XML file
# -------------------------------
tree = ET.ElementTree(configuration)
tree.write(output_config, encoding="utf-8", xml_declaration=True)

print(f"✅ SUMO config created: {output_config}")