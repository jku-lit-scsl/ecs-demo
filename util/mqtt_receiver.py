#!/usr/bin/env python
import logging

from paho.mqtt import client as mqtt_client

import config.config as CONFIG
from util.utils import singleton, get_current_time_in_millis

global receive_mqtt_client_id


def _set_globals():
    global receive_mqtt_client_id
    time_in_milli = get_current_time_in_millis()
    receive_mqtt_client_id = f'receiver-mqtt-{time_in_milli}'


def _on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker!")
    else:
        logging.error("Failed to connect, return code %d \n ", rc)


class _MQTTReceiver:

    def __init__(self):
        self.client = None
        self.connect_mqtt_receiver()

    def connect_mqtt_receiver(self):
        global receive_mqtt_client_id
        # Set Connecting Client ID
        client = mqtt_client.Client(receive_mqtt_client_id)
        client.on_connect = _on_connect
        client.connect(CONFIG.mqtt_conf['mqtt_ip_receive'], CONFIG.mqtt_conf['mqtt_port_receive'])
        client.on_message = self.on_message
        self.client = client
        logging.info('receiver mqtt is set up')

    def subscribe(self, topic: str):
        self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        logging.info('received mqtt message: ' + msg.topic + " -> " + msg.payload.decode())

    def loop(self):
        self.client.loop_forever()


@singleton
class MQTTReceiver:
    def __init__(self):
        logging.info('Generating new MQTT receiver')
        _set_globals()
        self.mqtt_local_client = _MQTTReceiver()

    def subscribe(self, topic: str):
        """Publishes a new message on the specified topic"""
        self.mqtt_local_client.subscribe(topic)

    def start_listening(self):
        self.mqtt_local_client.loop()
