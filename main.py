from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json

url = "http://rung.ddns.net:8050"
app = Flask(__name__)
CORS(app)


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


if __name__ == "__main__":
    app.run(debug=True)
