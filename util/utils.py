import datetime
import time
import uuid
from pathlib import Path

import pytz

PROJ_ROOT = proj_root = Path(__file__).parent.parent


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
