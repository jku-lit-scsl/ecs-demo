import logging
import threading
import time

from util.mqtt_forwarder import MQTTForwarder
from util.setup import CLOUD_SERVER, get_operating_mode
from util.utils import get_cpu_usage, get_virtual_memory


class MonitoringController:
    # the default frequency for measuring the cpu in seconds
    BASE_FREQUENCY = 1.0

    def __init__(self, defcon_handler):
        self.current_frequency = self.BASE_FREQUENCY
        self.stop_thread_flag = False
        self.defcon_handler = defcon_handler

    def set_new_frequency(self, new_frequency):
        """Sets a new monitoring frequency"""
        self.current_frequency = new_frequency

    def reset_frequency(self):
        """Sets a new monitoring frequency"""
        self.current_frequency = self.BASE_FREQUENCY

    def _monitor(self):
        # necessary for initial setup
        time.sleep(60)
        logging.info('Started CPU monitoring')
        outlier_counter = 0
        while not self.stop_thread_flag:
            cpu_usage = get_cpu_usage()
            cpu_usage_str = {
                'CPU-Usage': cpu_usage,
                'RAM-Usage': get_virtual_memory()
            }

            if cpu_usage > 30.0:
                if self.defcon_handler.current_state.id == 'defcon_5_normal':
                    outlier_counter += 1
                    logging.error(f'Exceeding current CPU threshold: {cpu_usage}')
                    if outlier_counter == 5:
                        outlier_counter = 0
                        self.defcon_handler.increase()
            if cpu_usage > 40.0:
                if self.defcon_handler.current_state.id == 'defcon_4_monitoring':
                    outlier_counter += 1
                    logging.error(f'Exceeding current CPU threshold: {cpu_usage}')
                    if outlier_counter == 5:
                        outlier_counter = 0
                        self.defcon_handler.increase()
            if cpu_usage > 50.0:
                if self.defcon_handler.current_state.id == 'defcon_3_adv_sec':
                    outlier_counter += 1
                    logging.error(f'Exceeding current CPU threshold: {cpu_usage}')
                    if outlier_counter == 5:
                        outlier_counter = 0
                        self.defcon_handler.increase()
            if cpu_usage > 60.0:
                if self.defcon_handler.current_state.id == 'defcon_2_restrict':
                    outlier_counter += 1
                    logging.error(f'Exceeding current CPU threshold: {cpu_usage}')
                    if outlier_counter == 5:
                        outlier_counter = 0
                        self.defcon_handler.increase()

            if get_operating_mode() != CLOUD_SERVER:
                mqtt_fw = MQTTForwarder()
                mqtt_fw.publish('sensor/cpu', cpu_usage_str)
            time.sleep(self.current_frequency)

    def start_monitoring(self):
        """Starts the monitoring"""
        monitoring_thread = threading.Thread(target=self._monitor)
        monitoring_thread.start()

    def stop_monitoring(self):
        self.stop_thread_flag = True

    # create function for continious monitoring
