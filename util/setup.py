import logging
import threading
import time

import config.config as CONFIG
from util.mqtt_forwarder import MQTTForwarder
from util.mqtt_receiver import MQTTReceiver
from util.web_socket_server import start_ws_server

CLOUD_SERVER = 0
EDGE_DEVICE = 1
HARDWARE_DEVICE = 2

OPERATING_MODE = None


def _setup_mqtt_forwarder():
    mqtt_fw = MQTTForwarder()
    time.sleep(5)  # todo: remove this, only for testing purposes
    mqtt_fw.publish('tester', 'msgpayload')


def _setup_mqtt_receiver():
    mqtt_receiver = MQTTReceiver()
    mqtt_receiver.subscribe('#')
    mqtt_receiver.start_listening()


def _setup_web_socket_server():
    start_ws_server()


def _setup_server():
    threading.Thread(target=_setup_mqtt_receiver).start()
    threading.Thread(target=_setup_web_socket_server).start()
    # TODO: setup websocket server


def _setup_client():
    threading.Thread(target=_setup_mqtt_forwarder).start()
    # TODO: setup websocket client


def setup():
    """Basic configs for the application """
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d\t%H:%M:%S',
        # for logging to file
        # handlers=[
        #     logging.FileHandler(f"output/{get_current_time()}_output.log"),
        #     logging.StreamHandler()
        # ]
    )

    global OPERATING_MODE

    # determine operating mode
    if CONFIG.network_conf['server_ip'] and len(CONFIG.network_conf['children_ips']) > 0:
        OPERATING_MODE = EDGE_DEVICE
    elif CONFIG.network_conf['server_ip'] and len(CONFIG.network_conf['children_ips']) == 0:
        OPERATING_MODE = HARDWARE_DEVICE
    elif CONFIG.network_conf['server_ip'] == '' and len(CONFIG.network_conf['children_ips']) > 0:
        OPERATING_MODE = CLOUD_SERVER

    logging.info(f'Set operating mode to {get_operating_string()}')

    # setup communication depending on operating mode
    if OPERATING_MODE == CLOUD_SERVER:
        _setup_server()
    elif OPERATING_MODE == EDGE_DEVICE:
        _setup_server()
        _setup_client()
    elif OPERATING_MODE == HARDWARE_DEVICE:
        _setup_client()


def is_operating_mode_valid() -> bool:
    return OPERATING_MODE == CLOUD_SERVER or OPERATING_MODE == EDGE_DEVICE or OPERATING_MODE == HARDWARE_DEVICE


def get_operating_string() -> str:
    if OPERATING_MODE == CLOUD_SERVER: return 'Cloud Server'
    if OPERATING_MODE == EDGE_DEVICE: return 'Edge Device'
    if OPERATING_MODE == HARDWARE_DEVICE: return 'Hardware Device'
    logging.warning('No operating mode set!')
    return 'Unknown Mode'
