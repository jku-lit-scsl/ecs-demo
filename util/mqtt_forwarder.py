#!/usr/bin/env python
import logging

from paho.mqtt import client as mqtt_client

import config.config as CONFIG
from util.utils import singleton, get_current_time_in_millis

global local_mqtt_client_id


def _set_globals():
    global local_mqtt_client_id
    time_in_milli = get_current_time_in_millis()
    local_mqtt_client_id = f'local-mqtt-{time_in_milli}'


def _on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker!")
    else:
        logging.error("Failed to connect, return code %d \n ", rc)


class _MQTTForwarder:

    def __init__(self):
        self.client = None
        self.connect_forward_mqtt()

    def connect_forward_mqtt(self):
        global local_mqtt_client_id
        # Set Connecting Client ID
        client = mqtt_client.Client(local_mqtt_client_id)
        client.on_connect = _on_connect
        client.connect(CONFIG.network_conf['my_ip'], 1883)
        self.client = client
        logging.info('local mqtt is set up')

    def publish_local(self, topic, message):
        self.client.publish(topic=topic, payload=str(message))


@singleton
class MQTTForwarder:
    def __init__(self):
        logging.info('Generating new MQTT Forwarder')
        _set_globals()
        self.mqtt_local_client = _MQTTForwarder()

    def publish(self, topic: str, message):
        """Publishes a new message on the specified topic"""
        self.mqtt_local_client.publish_local(topic, message)
