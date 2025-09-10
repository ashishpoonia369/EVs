import pandas as pd
from sumolib.net import readNet

# Load your SUMO network
net = readNet("2345net.net.xml")

# Read your CSV (make sure it has 'lat' and 'lon' columns)
df = pd.read_csv("low_battery_positions.csv")

# Convert GPS to SUMO x, y
df[["x", "y"]] = df.apply(lambda row: pd.Series(
    net.convertLonLat2XY(row["lon"], row["lat"])
), axis=1)

# Save to new CSV if needed
df.to_csv("mapped_10percent_locations.csv", index=False)
    