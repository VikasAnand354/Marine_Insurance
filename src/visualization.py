import os
import folium
import pandas as pd
from folium.plugins import MarkerCluster

# Load processed data
df = pd.read_csv("../data/marine_insurance_dataset.csv")

# Define working ship icons
ship_icons = {
    "High": "../images/ship.png",  # Red ship icon
    "Medium": "../images/amber-ship.png",  # Orange ship icon
    "Low": "../images/green-ship.png"  # Green ship icon
}

# Initialize map with a dark background for contrast
world_map = folium.Map(location=[0, 0], zoom_start=2, tiles="CartoDB dark_matter")

# Add marker clustering
marker_cluster = MarkerCluster().add_to(world_map)

# Loop through vessels and add them to the map
for _, row in df.iterrows():
    lat, lon = row["latitude"], row["longitude"]
    risk_level = row["risk_category"]
    ship_icon = ship_icons.get(risk_level, ship_icons["Low"])  # Default to low-risk icon if missing

    # Popup Information
    popup_text = f"""
    <b>Vessel:</b> {row['vessel_name']}<br>
    <b>Risk Level:</b> <span style='color:{risk_level.lower()};'>{risk_level}</span><br>
    <b>Speed:</b> {row['speed_knots']} knots<br>
    <b>Piracy Risk:</b> {row['piracy_risk']}<br>
    <b>War Zone Risk:</b> {row['war_zone_risk']}<br>

    """

    # Add custom ship marker
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.CustomIcon(ship_icon, icon_size=(40, 40))  # Ship icon with adjusted size
    ).add_to(marker_cluster)

# Ensure directory exists
output_path = "../visualizations/marine_risk_map.html"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save the map
world_map.save(output_path)
print(f"Map saved at {output_path}")
