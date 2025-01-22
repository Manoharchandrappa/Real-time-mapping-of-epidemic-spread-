import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv("epidemic_data.csv")

# Feature engineering: Calculate infection growth rate
data["infection_growth_rate"] = data["current_infected"] / (data["cumulative_infected"] + 1)

# Define features and target
features = [
    "current_infected", "deaths", "recovery_rate", "population_impact_percentage", "latitude", "longitude", "infection_growth_rate"
]
X = data[features]
y = data["location"]  # Predict the most likely next affected location

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save the model
with open("epidemic_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Updated prediction model saved as 'epidemic_model.pkl'.")
