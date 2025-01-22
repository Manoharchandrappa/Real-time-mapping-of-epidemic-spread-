import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Load the CSV file
csv_file = "epidemic_data.csv"
data = pd.read_csv(csv_file)

# Ensure 'location' column exists
if "location" not in data.columns:
    raise ValueError("The 'location' column is missing in the CSV file.")

# Initialize geolocator
geolocator = Nominatim(user_agent="epidemic_tracker")

def get_coordinates(location):
    """
    Fetch latitude and longitude for a given location using geopy.
    """
    try:
        loc = geolocator.geocode(location, timeout=10)
        if loc:
            return loc.latitude, loc.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        return None, None

# Add latitude and longitude columns
data["latitude"], data["longitude"] = zip(*data["location"].apply(get_coordinates))

# Save updated data to a new CSV file
updated_csv_file = "epidemic_data_with_coordinates.csv"
data.to_csv(updated_csv_file, index=False)
print(f"Updated CSV saved as {updated_csv_file}")
