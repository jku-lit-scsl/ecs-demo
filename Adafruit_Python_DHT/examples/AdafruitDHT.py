#!/usr/bin/python
import time

import Adafruit_DHT

from util.mqtt_forwarder import MQTTForwarder


def collect_dht22_data(mqtt_fw: MQTTForwarder):
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        mqtt_fw.publish('sensor/dht22', f'Temp={temperature}  Humidity={humidity}%')
        time.sleep(1)
