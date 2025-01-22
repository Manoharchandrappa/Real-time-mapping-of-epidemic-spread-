from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import numpy as np
import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Use your MySQL password
    database="epidemic_db"
)
cursor = conn.cursor()

app = Flask(__name__)

# Load epidemic data
try:
    epidemic_data = pd.read_csv("epidemic_data.csv")
except FileNotFoundError:
    print("Epidemic data file not found. Ensure 'epidemic_data.csv' exists.")
    epidemic_data = pd.DataFrame()

# Load the prediction model
try:
    with open("epidemic_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
except (FileNotFoundError, EOFError) as e:
    print(f"Error loading model: {e}")
    model = None

@app.route("/")
def landing():
    """
    Render the landing page.
    """
    return render_template("index.html")  # Assuming your landing page is named index.html

@app.route("/form")
def form():
    """
    Render the form page for data submission.
    """
    return render_template("form.html")  # Ensure 'form.html' exists in the templates directory

@app.route("/blog")
def blog():
    """
    Render the blog page.
    """
    return render_template("blog.html")

@app.route("/map-data")
def map_data():
    """
    Provide data for the map visualization.
    """
    if epidemic_data.empty:
        return jsonify({"error": "No epidemic data available"}), 404

    # Convert relevant columns to JSON
    map_data = epidemic_data[["latitude", "longitude", "location", "current_infected"]].to_dict(orient="records")
    return jsonify(map_data)

@app.route("/predict", methods=["GET"])
def predict_page():
    """
    Render the prediction page for user input.
    """
    return render_template("predict.html")

@app.route("/predict", methods=["POST"])
def predict_city():
    """
    Handle predictions based on city input.
    """
    try:
        data = request.json
        city = data.get("city", "")

        # Example prediction logic
        next_likely_city = "Hyderabad" if city == "Bangalore" else "Mumbai"
        second_wave_risk = "High" if city in ["Mumbai", "Delhi"] else "Low"
        advisory = "Avoid crowded areas; vaccination critical." if second_wave_risk == "High" else "General precautions advised."

        return jsonify({
            "next_likely_city": next_likely_city,
            "current_risk_level": "Moderate",
            "second_wave_risk": second_wave_risk,
            "advisory": advisory
        })
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": "An error occurred during prediction."}), 500


@app.route("/alert")
def alert():
    return render_template("alert.html")

@app.route("/alert-data")
def alert_data():
    # Get city from query parameter
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City not provided"}), 400

    # Filter epidemic data for the selected city
    city_data = epidemic_data[epidemic_data["location"].str.contains(city, case=False, na=False)]
    if city_data.empty:
        return jsonify({"error": "No data available for the selected city"}), 404

    # Extract relevant data
    data = city_data.iloc[0]
    risk_level = (
        "High" if data["current_infected"] > 5000 else
        "Moderate" if data["current_infected"] > 1000 else
        "Low"
    )
    advisory = (
        "Avoid crowded places and ensure vaccination." if risk_level == "High" else
        "Stay cautious and maintain hygiene." if risk_level == "Moderate" else
        "Minimal risk. Stay updated with local health guidelines."
    )

    return jsonify({
        "city": data["location"],
        "current_infected": int(data["current_infected"]),
        "deaths": int(data["deaths"]),
        "recovery_rate": round(data["recovery_rate"], 2),
        "risk_level": risk_level,
        "advisory": advisory
    })

if __name__ == "__main__":
    app.run(debug=True)