from flask import Flask, jsonify
import requests

url = "http://rung.ddns.net:8050"
app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)
