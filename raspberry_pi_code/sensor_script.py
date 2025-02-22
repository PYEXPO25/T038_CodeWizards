import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import json

# Pin Configuration
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO4
SOIL_SENSOR_PIN = 17  # GPIO17
RELAY_PIN = 27  # GPIO27 (Relay for Water Pump)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOIL_SENSOR_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH)  # Start with motor off

# MQTT Configuration for ThingsBoard
THINGSBOARD_HOST = 'demo.thingsboard.io'  # Change to your ThingsBoard server
ACCESS_TOKEN = 'QK0ahrybPRWm6KWfT6Rx'

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()

def get_sensor_data():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    soil_moisture = GPIO.input(SOIL_SENSOR_PIN)
    return temperature, humidity, soil_moisture

def control_motor(soil_moisture):
    if soil_moisture == 0:  # Soil is dry
        GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn ON pump
        send_alert("Motor Turned ON - Soil Dry")
    else:
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn OFF pump
        send_alert("Motor Turned OFF - Soil Moist")

def send_alert(message):
    print("Sending alert:", message)  # Replace with Twilio API for SMS/WhatsApp

try:
    while True:
        temp, hum, soil = get_sensor_data()
        control_motor(soil)

        data = {"temperature": temp, "humidity": hum, "soil_moisture": soil}
        client.publish("v1/devices/me/telemetry", json.dumps(data))

        print(f"Temperature: {temp}C, Humidity: {hum}%, Soil Moisture: {'Dry' if soil == 0 else 'Wet'}")
        time.sleep(10)  # Send data every 10 seconds

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on exit
