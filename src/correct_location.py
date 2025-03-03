import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# Load the dataset
file_path = "../data/marine_insurance_dataset.csv"  # Update with actual file path
df = pd.read_csv(file_path)

def get_region(lat, lon):
    """Fetches region name based on latitude and longitude using Nominatim."""
    geolocator = Nominatim(user_agent="geo_checker")
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True, timeout=10)
        if location and 'address' in location.raw:
            return location.raw['address'].get('country', 'Unknown')
    except GeocoderTimedOut:
        time.sleep(1)
        return get_region(lat, lon)
    except Exception:
        return 'Unknown'

# Apply geolocation function to update incorrect regions
df['detected_region'] = df.apply(lambda row: get_region(row['latitude'], row['longitude']), axis=1)

# Replace incorrect regions
df.loc[df['region'] != df['detected_region'], 'region'] = df['detected_region']

df.drop(columns=['detected_region'], inplace=True)

# Save the corrected file
df.to_csv("marine_insurance_dataset_corrected.csv", index=False)

print("Corrected dataset saved as 'marine_insurance_dataset_corrected.csv'")
