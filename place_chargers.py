"""
Simple helper to place charging stations from lon/lat onto the SUMO net
and produce an additional file `chargingStations_generated.add.xml`.

Requirements:
- sumolib (pip install sumolib)
- run the script from the folder containing your `*.net.xml` (or set paths)

Notes:
- This script assumes the network uses lon/lat coordinates. If your net is
  in projected coordinates, you'll need to convert the input coordinates.
"""
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sumolib.net
import math

# Edit these if your net filename differs
NET_FILE = "2345net.net.xml"
OUT_FILE = "chargingStations_generated.add.xml"

# Your station list (id, lon, lat)
stations = [
    ("station_1", 72.800870, 21.158818),
    ("station_2", 72.864481, 21.206786),
    ("station_3", 72.751914, 21.136598),
    ("station_4", 72.789163, 21.212759),
    ("station_5", 72.871406, 21.148910),
    ("station_6", 72.822842, 21.195128),
    ("station_7", 72.840619, 21.237041),
    ("station_8", 72.842267, 21.175541),
]

net = sumolib.net.readNet(NET_FILE)


def point_to_segment_dist(px, py, x1, y1, x2, y2):
    # distance from point p to segment (x1,y1)-(x2,y2)
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))
    projx = x1 + t * dx
    projy = y1 + t * dy
    return math.hypot(px - projx, py - projy)


def to_net_xy(net, lon, lat):
    # Try converting lon/lat to network coords if API available
    if hasattr(net, "convertLonLat2XY"):
        try:
            return net.convertLonLat2XY(lon, lat)
        except Exception:
            pass
    # fallback: assume net already uses lon/lat
    return (lon, lat)


def find_nearest_lane(net, x, y):
    best_lane = None
    best_d = float("inf")
    for edge in net.getEdges():
        try:
            lanes = edge.getLanes()
        except Exception:
            lanes = []
        for lane in lanes:
            try:
                shape = lane.getShape()
            except Exception:
                shape = None
            if not shape:
                try:
                    shape = edge.getShape()
                except Exception:
                    shape = None
            if not shape:
                continue
            # compute distance from point to each segment in shape
            for i in range(len(shape) - 1):
                x1, y1 = shape[i]
                x2, y2 = shape[i + 1]
                d = point_to_segment_dist(x, y, x1, y1, x2, y2)
                if d < best_d:
                    best_d = d
                    best_lane = lane
    return best_lane

root = ET.Element("additional")

for sid, lon, lat in stations:
    # Convert lon/lat to net coordinates if possible, then find nearest lane.
    x, y = to_net_xy(net, lon, lat)
    lane_obj = find_nearest_lane(net, x, y)
    if lane_obj is None:
        print(f"Warning: no lane found near {sid} ({lon},{lat}); skipping")
        continue
    lane = lane_obj.getID()

    # Create a basic chargingStation element. You can adjust attributes as needed.
    # Attributes used here are generic: pos (m from lane start), connectors, power_kW
    cs = ET.SubElement(root, "chargingStation")
    cs.set("id", sid)
    cs.set("lane", lane)
    cs.set("pos", "0")
    cs.set("connectors", "2")
    cs.set("power_kW", "22")

# pretty print
xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(xml_str)

print(f"Wrote {OUT_FILE}. Add this file to your configuration additional-files.")
print("If your net uses projected coords, convert lon/lat first or adapt the script.")