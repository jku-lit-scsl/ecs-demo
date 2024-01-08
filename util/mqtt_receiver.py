#!/usr/bin/env python
import logging

from paho.mqtt import client as mqtt_client

import config.config as CONFIG
from secure_mod.intrusion_detector import check_new_msg
from util.utils import singleton, get_current_time_in_millis

global receive_mqtt_client_id
is_ids_on = False


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
        client.connect(CONFIG.network_conf['my_ip'], 1883)
        client.on_message = self.on_message
        self.client = client
        logging.info('receiver mqtt is set up')

    def subscribe(self, topic: str):
        self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        global is_ids_on
        if is_ids_on:
            check_new_msg()

        # if 'cpu' in msg.topic:
        # logging.info('received mqtt message: ' + msg.topic + " -> " + msg.payload.decode())

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

    def set_ids(self, flag: bool):
        """
        Sets the MQTT IDS either on or off
        :param flag: boolean to set the IDS on (True) or off (False)
        :return: void
        """
        global is_ids_on
        is_ids_on = flag
