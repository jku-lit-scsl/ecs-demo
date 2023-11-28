#!/usr/bin/env python
import logging

from paho.mqtt import client as mqtt_client

from util.utils import get_config, singleton, get_current_time_in_millis

CONFIG = get_config()

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


class _MQTTForwarderLocal:

    def __init__(self):
        self.connect_local_mqtt()

    def connect_local_mqtt(self):
        global local_mqtt_client_id
        # Set Connecting Client ID
        client = mqtt_client.Client(local_mqtt_client_id)
        client.on_connect = _on_connect
        client.connect(CONFIG['mqtt_ip'], CONFIG['mqtt_port'])
        self.client = client
        logging.info('local mqtt is set up')

    def publish_local(self, topic, message):
        self.client.publish(topic, str(message))


@singleton
class MQTTForwarder:
    def __init__(self):
        logging.info('Generating new MQTT Forwarder')
        _set_globals()
        self.mqtt_local_client = _MQTTForwarderLocal()

    def publish(self, topic, message):
        self.mqtt_local_client.publish_local(topic, message)
