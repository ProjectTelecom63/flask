from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json

url = "http://rung.ddns.net:8050"
app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app


@app.route("/api/show", methods=["GET"])
def api_show():
    urlshow = url + "/api/show"

    try:
        response = requests.get(urlshow)
        response.raise_for_status()  # Check for errors in the response

        # Assuming the response is in JSON format
        data = response.json()

        return jsonify(data)
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return jsonify({"error": "Failed to get API response"}), 500


@app.route("/api/node", methods=["GET"])
def api_node():
    urlnode = url + "/api/node"

    try:
        response = requests.get(urlnode)
        response.raise_for_status()  # Check for errors in the response

        # Assuming the response is in JSON format
        data = response.json()

        return jsonify(data)
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return jsonify({"error": "Failed to get API response"}), 500


@app.route("/api/show/today", methods=["GET"])
def api_today():
    urlnode = url + "/api/show/today"

    try:
        response = requests.get(urlnode)
        response.raise_for_status()  # Check for errors in the response

        # Assuming the response is in JSON format
        data = response.json()

        return jsonify(data)
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return jsonify({"error": "Failed to get API response"}), 500


@app.route("/api/activate", methods=["GET"])
def activate():
    try:
        nodename = request.args.get("nodename")
        urlact = url + "/api/activate?nodename=" + nodename
        response = requests.get(urlact)
        response.raise_for_status()

        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return jsonify({"error": "Failed to get API response"}), 500


@app.route("/api/date", methods=["POST"])
def fetch_data():
    try:
        urldate = url + "/api/date"
        start = request.json.get("start")
        end = request.json.get("end")
        print(f"Received POST data - Start Datetime: {start}, End Datetime: {end}")
        payload = {"start": start, "end": end}

        headers = {"Content-Type": "application/json"}

        response = requests.post(urldate, json=payload, headers=headers)

        data = response.json()
        return jsonify(data)

    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return jsonify({"error": "Failed to get API response"}), 500


@app.route("/api/alert/changecon", methods=["POST"])
def change_con():
    try:
        data = request.json
        print(data)
        urlcon = url + "/api/alert/changecon"
        print(urlcon)
        temperature = data.get("Temperature")
        humidity = data.get("Humidity")
        speed = data.get("Speed")
        longitude = data.get("Longitude")
        latitude = data.get("Latitude")
        radius = data.get("Radius")
        nbat = data.get("NBattery")
        gbat = data.get("GBattery")
        payload = {
            "Temperature": temperature,
            "Humidity": humidity,
            "Speed": speed,
            "Longitude": longitude,
            "Latitude": latitude,
            "Radius": radius,
            "NBattery": nbat,
            "GBattery": gbat,
        }
        print(payload)
        headers = {"Content-Type": "application/json"}

        requests.post(urlcon, json=payload, headers=headers)

        return jsonify(data)

    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return jsonify({"error": "Failed to get API response"}), 500


@app.route("/api/alert/con", methods=["GET"])
def con():
    try:
        urlcon = url + "/api/alert/con"
        response = requests.get(urlcon)
        response.raise_for_status()  # Check for errors in the response

        # Assuming the response is in JSON format
        data = response.json()

        return jsonify(data)
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return jsonify({"error": "Failed to get API response"}), 500


@app.route("/api/addemail", methods=["POST"])
def insert_email():
    try:
        data = request.json
        print(data)
        urlcon = url + "/api/alert/addemail"
        print(urlcon)
        email = request.json.get("email", None)
        delay = request.json.get("delay", None)
        payload = {
            "email": email,
            "delay": delay,
        }
        print(payload)
        headers = {"Content-Type": "application/json"}

        requests.post(urlcon, json=payload, headers=headers)

        return jsonify(data)

    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return jsonify({"error": "Failed to get API response"}), 500


@app.route("/api/deleteemail", methods=["POST"])
def delete_email():
    urldel = url + "/api/deleteemail"
    try:
        email = request.json.get("email")
        payload = {"email": email}
        print(payload)
        headers = {"Content-Type": "application/json"}

        response = requests.post(urldel, json=payload, headers=headers)

        data = response.json()
        return jsonify(data)

    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return jsonify({"error": "Failed to get API response"}), 500

@app.route("/api/emails", methods=["GET"])
def get_emails():
    try:
        urlget = url + "/api/emails"
        response = requests.get(urlget)
        response.raise_for_status()  # Check for errors in the response

        # Assuming the response is in JSON format
        data = response.json()

        return jsonify(data)
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        return jsonify({"error": "Failed to get API response"}), 500


if __name__ == "__main__":
    app.run(debug=True)
