import logging
import threading

import config.config as CONFIG
from Adafruit_Python_DHT.examples.AdafruitDHT import collect_dht22_data
from util.mqtt_receiver import MQTTReceiver
from util.web_socket_server import start_ws_server

CLOUD_SERVER = 0
FOG_DEVICE = 1
EDGE_DEVICE = 2

OPERATING_MODE = None

mqtt_receiver = None


def _setup_mqtt_forwarder():
    if CONFIG.network_conf['my_ip'] == '192.168.68.61':
        collect_dht22_data()


def _setup_mqtt_receiver():
    global mqtt_receiver
    mqtt_receiver = MQTTReceiver()


def get_mqtt_receiver():
    global mqtt_receiver
    return mqtt_receiver


def _setup_server():
    global OPERATING_MODE
    _setup_mqtt_receiver()
    threading.Thread(target=start_ws_server, args=(OPERATING_MODE,)).start()
    # TODO: setup websocket server


def _setup_client():
    threading.Thread(target=_setup_mqtt_forwarder).start()
    # TODO: setup websocket client


def setup():
    """Basic configs for the application """
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',  # Custom format with timestamp
        datefmt='%Y-%m-%d    %H:%M:%S'  # Date format for the timestamp
        # for logging to file
        # handlers=[
        #     logging.FileHandler(f"output/{get_current_time()}_output.log"),
        #     logging.StreamHandler()
        # ]
    )
    # set log level to info
    logging.getLogger().setLevel(logging.INFO)

    global OPERATING_MODE

    # determine operating mode
    if CONFIG.network_conf['server_ip'] and len(CONFIG.network_conf['client_ips']) > 0:
        OPERATING_MODE = FOG_DEVICE
    elif CONFIG.network_conf['server_ip'] and len(CONFIG.network_conf['client_ips']) == 0:
        OPERATING_MODE = EDGE_DEVICE
    elif CONFIG.network_conf['server_ip'] == '' and len(CONFIG.network_conf['client_ips']) > 0:
        OPERATING_MODE = CLOUD_SERVER

    logging.info(f'Set operating mode to {get_operating_string()}')
    logging.info(f"my_ip = {CONFIG.network_conf['my_ip']}")
    logging.info(f"server_ip = {CONFIG.network_conf['server_ip']}")
    logging.info(f"client_ips = {CONFIG.network_conf['client_ips']}")

    # setup communication depending on operating mode
    if OPERATING_MODE == CLOUD_SERVER:
        _setup_server()
    elif OPERATING_MODE == FOG_DEVICE:
        _setup_server()
        _setup_client()
    elif OPERATING_MODE == EDGE_DEVICE:
        _setup_client()


def is_operating_mode_valid() -> bool:
    global OPERATING_MODE
    return OPERATING_MODE == CLOUD_SERVER or OPERATING_MODE == EDGE_DEVICE or OPERATING_MODE == FOG_DEVICE


def get_operating_mode():
    global OPERATING_MODE
    return OPERATING_MODE


def get_operating_string() -> str:
    global OPERATING_MODE
    if OPERATING_MODE == CLOUD_SERVER: return 'Cloud Server'
    if OPERATING_MODE == EDGE_DEVICE: return 'Edge Device'
    if OPERATING_MODE == FOG_DEVICE: return 'Fog Device'
    logging.warning('No operating mode set!')
    return 'Unknown Mode'
