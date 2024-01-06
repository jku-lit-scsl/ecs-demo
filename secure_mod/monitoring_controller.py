import threading
import time

import psutil

from util.mqtt_forwarder import MQTTForwarder


def get_cpu_usage() -> float:
    """Returns the CPU usage in percent"""
    return psutil.cpu_percent(interval=None)


def get_virtual_memory() -> float:
    """Returns the memory usage in percent"""
    return psutil.virtual_memory().percent
    # you can calculate percentage of available memory
    # psutil.virtual_memory().available * 100 / psutil.virtual_memory().total


class MonitoringController():
    # the default frequency for measuring the cpu in seconds
    BASE_FREQUENCY = 1.0

    def __init__(self, mqtt_fw: MQTTForwarder):
        self.current_frequency = self.BASE_FREQUENCY
        self.stop_thread_flag = False
        self.mqtt_fw = mqtt_fw

    def set_new_frequency(self, new_frequency):
        """Sets a new monitoring frequency"""
        self.current_frequency = new_frequency

    def reset_frequency(self):
        """Sets a new monitoring frequency"""
        self.current_frequency = self.BASE_FREQUENCY

    def _monitor(self):
        while not self.stop_thread_flag:
            # TODO: forward the message somehow to the knowledge base when in other defcon mode
            self.mqtt_fw.publish('sensor/cpu', f'CPU-Usage={get_cpu_usage()} RAM-Usage={get_virtual_memory()}')
            time.sleep(self.current_frequency)

    def start_monitoring(self):
        """Starts the monitoring"""
        monitoring_thread = threading.Thread(target=self._monitor)
        monitoring_thread.start()

    def stop_monitoring(self):
        self.stop_thread_flag = True

    # create function for continious monitoring
