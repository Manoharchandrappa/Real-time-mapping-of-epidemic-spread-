import pandas as pd
from geopy.geocoders import Nominatim
import random
import time

# List of countries and cities (you can expand this list)
countries_cities = {
    "USA": ["New York", "San Francisco", "Los Angeles", "Chicago", "Houston"],
    "India": ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"],
    "UK": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow"],
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
    "Brazil": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador", "Fortaleza"],
    "France": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"],
    "South Africa": ["Cape Town", "Johannesburg", "Durban", "Pretoria", "Port Elizabeth"],
    "Germany": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"]
}

# Initialize geolocator
geolocator = Nominatim(user_agent="epidemic_tracker")


# Function to get latitude and longitude
def get_coordinates(city, country):
    try:
        location = geolocator.geocode(f"{city}, {country}", timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching coordinates for {city}, {country}: {e}")
        return None, None


# Create empty list to store generated data
data = []

# Generate data for each country and city
for country, cities in countries_cities.items():
    for city in cities:
        latitude, longitude = get_coordinates(city, country)
        if latitude and longitude:
            # Simulate epidemic data
            current_infected = random.randint(1000, 10000)
            deaths = random.randint(50, 500)
            recovery_rate = round(random.uniform(80, 95), 2)
            population_impact_percentage = round(random.uniform(0.5, 3.0), 2)

            # Add row to data list
            data.append({
                "location": city,
                "country": country,
                "latitude": latitude,
                "longitude": longitude,
                "current_infected": current_infected,
                "deaths": deaths,
                "recovery_rate": recovery_rate,
                "population_impact_percentage": population_impact_percentage
            })

        # To avoid hitting the geocoding API too quickly, add a small delay
        time.sleep(1)

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV file
df.to_csv("epidemic_data.csv", index=False)

print("Data generated and saved to epidemic_data1.csv")
