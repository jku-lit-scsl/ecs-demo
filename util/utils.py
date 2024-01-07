import datetime
import json
import threading
import time
import uuid
from pathlib import Path

import pytz

from util.web_socket_client import send_msg_websocket

PROJ_ROOT = proj_root = Path(__file__).parent.parent


def update_knowledge_base(defcon_lvl):
    """
    Takes the defcon level as param and saves it locally and, if possible, sends it to the parent system
    :param defcon_lvl: the new defcon level to be stored
    :return: void
    """
    # TODO: save in local knowledgebase
    msg = {'defcon_lvl': defcon_lvl}
    threading.Thread(target=send_msg_websocket, args=(json.dumps(msg),)).start()


def get_current_time_in_millis():
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
