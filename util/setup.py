import logging
import os
import threading
import time

import config.config as CONFIG
from Adafruit_Python_DHT.examples.AdafruitDHT import collect_dht22_data
from util.mqtt_receiver import MQTTReceiver
from util.utils import start_mosquitto_service, synchronize_system_time, get_cpu_usage, generate_timestamp_for_filename
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
    # ensure that mosquitto is running
    start_mosquitto_service()

    global OPERATING_MODE
    _setup_mqtt_receiver()
    threading.Thread(target=start_ws_server, args=(OPERATING_MODE,)).start()


def _setup_client():
    threading.Thread(target=_setup_mqtt_forwarder).start()


def log_cpu_usage_every_second():
    while True:
        # Get the current time
        current_time = time.time()

        # Calculate how long to sleep to wake up at the next full second
        sleep_time = 1 - (current_time % 1)

        # Sleep until the next full second
        time.sleep(sleep_time)

        # Log the message
        logging.info(f'CPU usage in percent: >{get_cpu_usage()}<')


def setup_logging():
    # Remove any existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Create a StreamHandler for console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)

    # Create a FileHandler for logging to a file
    log_file_path = os.path.join('logs',
                                 f"{generate_timestamp_for_filename()}_{CONFIG.network_conf['my_ip']}_efficacy_eval.log")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    file_handler = logging.FileHandler(log_file_path, mode='w')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                                       '%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_formatter)

    # Add both handlers to the root logger
    logger = logging.getLogger()
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    threading.Thread(target=log_cpu_usage_every_second).start()


def setup():
    """Basic configs for the application """
    global OPERATING_MODE

    setup_logging()

    synchronize_system_time()

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
