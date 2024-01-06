import logging
import threading

import config.config as CONFIG
from Adafruit_Python_DHT.examples.AdafruitDHT import collect_dht22_data
from util.mqtt_forwarder import MQTTForwarder
from util.mqtt_receiver import MQTTReceiver
from util.web_socket_server import start_ws_server

CLOUD_SERVER = 0
FOG_DEVICE = 1
EDGE_DEVICE = 2

OPERATING_MODE = None


def _setup_mqtt_forwarder(mqtt_fw: MQTTForwarder):
    if CONFIG.network_conf['my_ip'] == '192.168.68.61':
        collect_dht22_data(mqtt_fw)


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


def _setup_client(mqtt_fw: MQTTForwarder):
    threading.Thread(target=_setup_mqtt_forwarder, args=(mqtt_fw,)).start()
    # TODO: setup websocket client


def setup(mqtt_fw: MQTTForwarder):
    """Basic configs for the application """
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d\t%H:%M:%S',
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
        _setup_client(mqtt_fw)
    elif OPERATING_MODE == EDGE_DEVICE:
        _setup_client(mqtt_fw)


def is_operating_mode_valid() -> bool:
    return OPERATING_MODE == CLOUD_SERVER or OPERATING_MODE == EDGE_DEVICE or OPERATING_MODE == FOG_DEVICE


def get_operating_string() -> str:
    if OPERATING_MODE == CLOUD_SERVER: return 'Cloud Server'
    if OPERATING_MODE == EDGE_DEVICE: return 'Edge Device'
    if OPERATING_MODE == FOG_DEVICE: return 'Fog Device'
    logging.warning('No operating mode set!')
    return 'Unknown Mode'
