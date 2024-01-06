#!/usr/bin/python
import time

from util.mqtt_forwarder import MQTTForwarder


def collect_dht22_data(mqtt_fw: MQTTForwarder):
    while True:
        mqtt_fw.publish('Temp={10.0} Humidity={15.0}')
        time.sleep(1)
