from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import firebase_admin
from firebase_admin import auth, credentials
import requests
import paho.mqtt.client as mqtt
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Firebase Setup
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)

# ThingsBoard Credentials
THINGSBOARD_HOST = "demo.thingsboard.io"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

# Twilio Credentials
TWILIO_ACCOUNT_SID = "ACb18b00fb63b2459926ce5605293f158c"
TWILIO_AUTH_TOKEN = "90efcc6a88b616f50cdddb4fba9216f7"
TWILIO_PHONE_NUMBER = "+12197323694"
USER_PHONE_NUMBER = "+918248930835"

# MQTT Setup
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(ACCESS_TOKEN)
mqtt_client.connect(THINGSBOARD_HOST, 1883, 60)

# Sample Motor Activity Logs
motor_logs = [
    {"timestamp": "2025-02-21 12:00 PM", "status": "ON"},
    {"timestamp": "2025-02-21 12:15 PM", "status": "OFF"},
]

# Function to fetch sensor data from ThingsBoard
def get_sensor_data():
    url = f"https://{THINGSBOARD_HOST}/api/plugins/telemetry/DEVICE/{ACCESS_TOKEN}/values/timeseries"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data.get("temperature", [{}])[0].get("value", "N/A")
        humidity = data.get("humidity", [{}])[0].get("value", "N/A")
        soil_moisture = data.get("soil_moisture", [{}])[0].get("value", "N/A")
        return {"temperature": temperature, "humidity": humidity, "soil_moisture": soil_moisture}
    return None

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = auth.get_user_by_email(email)
            session["user"] = user.uid
            return redirect(url_for("dashboard"))
        except:
            return "Login Failed!"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    
    data = get_sensor_data()
    return render_template("dashboard.html", data=data)

@app.route("/notifications")
def notifications():
    return render_template("notifications.html", logs=motor_logs)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import firebase_admin
from firebase_admin import auth, credentials
import requests
import paho.mqtt.client as mqtt
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Firebase Setup
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)

# ThingsBoard Credentials
THINGSBOARD_HOST = "demo.thingsboard.io"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

# Twilio Credentials
TWILIO_ACCOUNT_SID = "ACb18b00fb63b2459926ce5605293f158c"
TWILIO_AUTH_TOKEN = "90efcc6a88b616f50cdddb4fba9216f7"
TWILIO_PHONE_NUMBER = "+12197323694"
USER_PHONE_NUMBER = "+918248930835"


# MQTT Setup
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(ACCESS_TOKEN)
mqtt_client.connect(THINGSBOARD_HOST, 1883, 60)

# Sample Motor Activity Logs
motor_logs = [
    {"timestamp": "2025-02-21 12:00 PM", "status": "ON"},
    {"timestamp": "2025-02-21 12:15 PM", "status": "OFF"},
]

# Function to fetch sensor data from ThingsBoard
def get_sensor_data():
    url = f"https://{THINGSBOARD_HOST}/api/plugins/telemetry/DEVICE/{ACCESS_TOKEN}/values/timeseries"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data.get("temperature", [{}])[0].get("value", "N/A")
        humidity = data.get("humidity", [{}])[0].get("value", "N/A")
        soil_moisture = data.get("soil_moisture", [{}])[0].get("value", "N/A")
        return {"temperature": temperature, "humidity": humidity, "soil_moisture": soil_moisture}
    return None

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = auth.get_user_by_email(email)
            session["user"] = user.uid
            return redirect(url_for("dashboard"))
        except:
            return "Login Failed!"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    
    data = get_sensor_data()
    return render_template("dashboard.html", data=data)

@app.route("/notifications")
def notifications():
    return render_template("notifications.html", logs=motor_logs)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
