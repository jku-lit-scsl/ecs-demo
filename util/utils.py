import datetime
import json
import logging
import os.path
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

import pytz

from util.web_socket_client import send_msg_websocket

PROJ_ROOT = proj_root = Path(__file__).parent.parent


def synchronize_system_time(ntp_server="pool.ntp.org"):
    """
    Synchronizes the system time with the specified NTP server.

    :param ntp_server: The NTP server to synchronize with. Defaults to 'pool.ntp.org'.
    """
    try:
        # Check if ntpd or chrony is installed
        ntp_installed = subprocess.run(["which", "ntpd"], stdout=subprocess.DEVNULL).returncode == 0
        chrony_installed = subprocess.run(["which", "chronyd"], stdout=subprocess.DEVNULL).returncode == 0

        if ntp_installed:
            # Stop the NTP service, synchronize the time, and start the service again
            subprocess.run(["sudo", "service", "ntp", "stop"], check=True)
            subprocess.run(["sudo", "ntpd", "-gq"], check=True)
            subprocess.run(["sudo", "service", "ntp", "start"], check=True)
        elif chrony_installed:
            # Using chrony to synchronize time
            subprocess.run(["sudo", "chronyc", "makestep"], check=True)
        else:
            logging.error("No NTP synchronization tool (ntpd or chrony) is installed.")
            sys.exit(1)

        logging.info("Time synchronization complete.")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


def generate_timestamp_for_filename():
    """
    Generates a timestamp string suitable for use in filenames.

    :return: A string representing the current date and time in a filename-safe format.
    """
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


latency_log_file = f"{generate_timestamp_for_filename()}_log_file.txt"


def start_mosquitto_service():
    try:
        subprocess.run(["sudo", "systemctl", "start", "mosquitto.service"], check=True)
        logging.info("Mosquitto service started successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while starting Mosquitto service: {e}")


def heartbeat_updater(defcon_handler, defcon_level, ip, sleep_timer):
    while True:
        send_update_knowledge_base(defcon_handler, defcon_level, ip)
        time.sleep(sleep_timer)


def send_update_knowledge_base(defcon_handler, defcon_level, ip):
    """
    Takes the defcon level as param and saves it locally and, if possible, sends it to the parent system
    :param defcon_handler: the defcon handler object
    :param defcon_level: the new defcon level to be stored
    :return: void
    """
    msg = {
        'defcon_lvl': defcon_level,
        'ip': ip
    }
    threading.Thread(target=send_msg_websocket, args=(json.dumps(msg), defcon_handler,)).start()


def write_latency_log(log_string: str, file_name=os.path.join(PROJ_ROOT, latency_log_file)):
    """
    Appends the given log string to a log file.

    :param log_string: The log message to write to the file.
    :param file_name: The name of the file to which the log will be written. Default is the latency logfile generated with a timestamp
    """
    with open(file_name, "a") as file:
        file.write(f'{generate_timestamp_for_filename}    {log_string}\n')


def log_latency(mqtt_msg):
    if 'cpu' in mqtt_msg.topic or 'dht22' in mqtt_msg.topic:
        # logging.info('received mqtt message: ' + mqtt_msg.topic + " -> " + mqtt_msg.payload.decode())
        msg_obj = json.loads(mqtt_msg.payload.decode())
        latency_for_msg = get_current_time_in_millis() - int(msg_obj['timestamp_sent'])
        logging.info(f'latency: {latency_for_msg}')
        write_latency_log(str(latency_for_msg))


def get_current_time_in_millis() -> int:
    """Returns the current time in milliseconds"""
    return time.time_ns() // 1_000_000


def singleton(class_):
    """Introduces a singleton decorator"""

    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


class Singleton(type):
    """Impl. of a singleton design pattern"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def generate_unique_id():
    """Returns a unique id"""
    return uuid.uuid4().__str__()


def get_current_time():
    """Returns the current time"""
    tz = pytz.timezone('Europe/Vienna')
    return datetime.datetime.now(tz).__str__()
