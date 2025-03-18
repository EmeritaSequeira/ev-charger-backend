from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from waitress import serve  # Install: pip install waitress

app = Flask(__name__)
CORS(app)  # Enable CORS

# Open Charge Map API details
API_URL = "https://api.openchargemap.io/v3/poi/"
API_KEY = "de00ccc8-3c6d-4299-a85e-1e95fbc6dcb9"  # Replace with your valid API Key

@app.route("/", strict_slashes=False)
def home():
    """Welcome message for API"""
    return jsonify({"message": "Welcome to the EV Charging Finder API!"})

@app.route("/stations", methods=["GET"], strict_slashes=False)
def get_stations():
    """Fetch nearby EV charging stations based on user's location"""
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    
    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude are required"}), 400

    try:
        url = f"{API_URL}?key={API_KEY}&latitude={lat}&longitude={lon}&distance=10&distanceunit=KM"
        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data"}), response.status_code

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting EV Charging Finder API...")
    serve(app, host="0.0.0.0", port=5000)  # Use Waitress for production
