import xml.etree.ElementTree as ET
import uuid

battery_file = "battery222_output.xml"
output_poi_file = "battery222last_drop_points.poi.xml"

ev_data = {}

with open(output_poi_file, 'w') as out:
    out.write('<additional>\n')

    for event, elem in ET.iterparse(battery_file, events=("start", "end")):
        if elem.tag == 'timestep' and event == "start":
            continue

        if elem.tag == 'vehicle' and event == "end":
            veh_id = elem.attrib.get('id')
            actual = elem.attrib.get('actualBatteryCapacity')
            max_cap = elem.attrib.get('maximumBatteryCapacity')
            x = elem.attrib.get('x')
            y = elem.attrib.get('y')

            if not all([veh_id, actual, max_cap, x, y]):
                elem.clear()
                continue

            actual = float(actual)
            max_cap = float(max_cap)

            if max_cap == 0 or veh_id in ev_data:
                elem.clear()
                continue

            battery_percent = actual / max_cap
            if battery_percent <= 0.1:
                ev_data[veh_id] = True
                unique_id = str(uuid.uuid4())[:8]  # Short unique ID
                # Larger POIs (width=5, height=5, bright red)
                out.write(
                    f'<poi id="evLow_{unique_id}" x="{x}" y="{y}" '
                    f'color="1,0,0" layer="1" width="50" height="50"/>\n'
                )

            elem.clear()

    out.write('</additional>\n')

print(f"✅ POI file generated: {output_poi_file}")