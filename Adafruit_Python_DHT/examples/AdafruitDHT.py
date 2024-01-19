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

critical_qos = 0
sleep_time = 1


def set_qos_temperature(qos):
    """
    Sets the QoS attribute for publishing the temperature measurements.
    :param qos: QoS as number, either 0, 1, 2
    :return: void
    """
    global critical_qos
    critical_qos = qos


def set_sleep_time(new_time):
    global sleep_time
    sleep_time = new_time


def collect_dht22_data():
    global sleep_time
    mqtt_fw = MQTTForwarder()

    while True:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        msg = {
            'humidity': humidity,
            'temperature': temperature,
        }
        mqtt_fw.publish('sensor/dht22', msg, critical_qos)
        time.sleep(sleep_time)
