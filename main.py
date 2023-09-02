from flask import Flask, render_template, request, jsonify, render_template_string
from datetime import datetime
import mysql.connector
import pytz
import folium

app = Flask(__name__)

# List to store the values
values_list = []

# Default configuration values
syncword = 128
tx_power = 10
freq = 915
interval = 15

# Replace these values with your actual database credentials
db_config = {
    "host": "containers-us-west-133.railway.app",
    "user": "root",
    "password": "0PA9tKDCgxMvvZC5YiOT",
    "port": 7131,
    "database": "railway",
    "auth_plugin": "mysql_native_password",
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/data", methods=["GET"]) #http://192.168.1.3:5000/insert_data?nodename=Node1&temperature=25.5&humidity=60.0&latitude=37.123456&longitude=-122.987654
def insert_data():
    now = datetime.now(pytz.timezone('Asia/Bangkok'))
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    nodename = request.args.get("nodename")
    temperature = request.args.get("temperature")
    humidity = request.args.get("humidity")
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")

    if nodename is not None and temperature is not None and humidity is not None:
        nodename = request.args.get("nodename")
        temperature = float(request.args.get("temperature"))
        humidity = float(request.args.get("humidity"))
        latitude = request.args.get("latitude")
        longitude = request.args.get("longitude")
        try:
            connection = mysql.connector.connect(**db_config)
            if connection.is_connected():
                print("Connected to the MySQL database")

                data_to_insert = {
                    "Time": time,
                    "Nodename": nodename,
                    "Temperature": temperature,
                    "Humidity": humidity,
                    "Latitude": latitude,
                    "Longitude": longitude,
                }

                cursor = connection.cursor()

                query = """
                INSERT INTO Data (Time, Nodename, Temperature, Humidity, Latitude, Longitude)
                VALUES (%(Time)s, %(Nodename)s, %(Temperature)s, %(Humidity)s, %(Latitude)s, %(Longitude)s)
                """

                cursor.execute(query, data_to_insert)
                connection.commit()

                print("Data inserted successfully")
        finally:
            if "connection" in locals() and connection.is_connected():
                connection.close()
                print("Connection closed")
                return "Data inserted successfully"
    else:
        return "Invalid data"

@app.route("/config")
def index():
    return render_template("config.html")


@app.route("/showconfig")
def show_config():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to the MySQL database")

            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT * FROM Configuration
            """

            cursor.execute(query)
            rows = cursor.fetchall()
            print(rows)

            return jsonify(rows[0])

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred"}), 500

    finally:
        if "connection" in locals() and connection.is_connected():
            connection.close()
            print("Connection closed")


@app.route("/sendconfig", methods=["POST"])
def send_config():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to the MySQL database")

            # Get data from the POST request
            data = request.form
            syncword = data.get("syncword")
            tx_power = data.get("txPower")
            freq = data.get("freq")
            interval = data.get("interval")
            hexnumber = hex(int(syncword)).upper()

            data_to_insert = {
                "Syncword": syncword,
                "Tx_power": tx_power,
                "Frequency": freq,
                "Tx_interval": interval,
            }

            cursor = connection.cursor()

            query = """
            INSERT INTO Configuration (id, Syncword, Tx_power, Frequency, Tx_interval)
            VALUES (1, %(Syncword)s, %(Tx_power)s, %(Frequency)s, %(Tx_interval)s)
            ON DUPLICATE KEY UPDATE
            Syncword = VALUES(Syncword),
            Tx_power = VALUES(Tx_power),
            Frequency = VALUES(Frequency),
            Tx_interval = VALUES(Tx_interval)
            """

            cursor.execute(query, data_to_insert)
            connection.commit()

            print("Data inserted successfully")

            return jsonify({"message": "Data inserted successfully"})

    finally:
        if "connection" in locals() and connection.is_connected():
            connection.close()
            print("Connection closed")

    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LoRa Parameter</title>
    </head>
    <body>
        <h1>Configuration Result</h1>
        <p>Syncword : {{ syncword }} ({{hexnumber}})</p>
        <p>Tx Power : {{ tx_power }} dBm</p>
        <p>Frequency : {{ freq }} MHz</p>
        <p>Interval : {{ interval }} minutes</p>
    </body>
    </html>
    """

    return render_template_string(
        template,
        hexnumber=hexnumber,
        syncword=syncword,
        tx_power=tx_power,
        freq=freq,
        interval=interval,
    )


@app.route("/show")
def show_values():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to the MySQL database")

            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT * FROM Data
            """

            cursor.execute(query)
            rows = cursor.fetchall()
            print(rows)

            return jsonify(rows)

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred"}), 500

    finally:
        if "connection" in locals() and connection.is_connected():
            connection.close()
            print("Connection closed")


@app.route('/delete', methods=['GET'])
def delete_values():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to the MySQL database")

            cursor = connection.cursor()

            # SQL query to delete all data from the table
            query = """
            DELETE FROM Data
            """

            cursor.execute(query)
            connection.commit()
            # Reset the auto-increment counter to start from 1
            reset_auto_increment_query = "ALTER TABLE Data AUTO_INCREMENT = 1"
            cursor.execute(reset_auto_increment_query)
            connection.commit()
            print("Auto-increment counter reset to 1.")

            return "All data deleted successfully"

    except Exception as e:
        print("Error:", e)
        return "An error occurred", 500

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Connection closed")

    return "All values deleted successfully!"

@app.route("/plot_locations")
def plot_locations():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to the MySQL database")

            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT Latitude, Longitude FROM Data
            """

            cursor.execute(query)
            rows = cursor.fetchall()
            print(rows)
            import os
            cwd = os.getcwd()
            # cwd = os.path.join(cwd,"Server")
            print(cwd)
            # Create a Leaflet map
            map = folium.Map(location=[rows[0]["Latitude"], rows[0]["Longitude"]], zoom_start=20)
            import shutil
            # Add markers for each location
            Latitudels  = []
            Longitudels = [] 
            for row in rows:
                Latitudels.append(row["Latitude"])
                Longitudels.append(row["Longitude"])
                folium.Marker([row["Latitude"], row["Longitude"]]).add_to(map)
            print(Latitudels)
            print(Longitudels)
            # Save the map to an HTML file (or you can return it as HTML)
            map.save("map.html")
            filehtml = os.path.join(cwd,"map.html")
            print(filehtml)
            dir_name = os.path.join(cwd, "templates")
            existing_file_path = os.path.join(dir_name,"map.html")
            print(dir_name)
            if os.path.exists(existing_file_path):
                os.remove(existing_file_path)
            shutil.move(filehtml, dir_name)

            return render_template("map.html")

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred"}), 500

    finally:
        if "connection" in locals() and connection.is_connected():
            connection.close()
            print("Connection closed")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
