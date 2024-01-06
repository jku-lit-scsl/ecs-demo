#!/usr/bin/python
import logging
import time

try:
    import Adafruit_DHT
except ModuleNotFoundError as e:
    # Handle the case where Adafruit_DHT is not found
    if str(e) == "No module named 'Adafruit_DHT'":
        logging.info("Adafruit_DHT module not found. Continuing without it.")
    else:
        # If the exception is for a different module, re-raise it
        raise

from util.mqtt_forwarder import MQTTForwarder


def collect_dht22_data():
    mqtt_fw = MQTTForwarder()

    while True:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        msg = {
            'humidity': humidity,
            'temperature': temperature,
        }
        mqtt_fw.publish('sensor/dht22', msg)
        time.sleep(1)
