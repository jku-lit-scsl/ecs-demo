import threading
import time

from util.mqtt_forwarder import MQTTForwarder
from util.mqtt_receiver import MQTTReceiver
from util.utils import setup


def _setup_mqtt_forwarder():
    mqtt_fw = MQTTForwarder()
    time.sleep(5)
    mqtt_fw.publish('tester', 'msgpayload')


def _setup_mqtt_receiver():
    mqtt_receiver = MQTTReceiver()
    mqtt_receiver.subscribe('#')
    mqtt_receiver.start_listening()


if __name__ == '__main__':
    setup()
    # mqtt_fw = MQTTForwarder()
    # mqtt_fw.publish("python/test", f"{get_current_time_in_millis()}")
    #
    # defcon_handler = DefconHandler()
    #
    # time.sleep(6)
    # defcon_handler.increase()

    # print(config.config.network_conf['my_ip'])

    forwarder_thread = threading.Thread(target=_setup_mqtt_forwarder)
    receiver_thread = threading.Thread(target=_setup_mqtt_receiver)
    forwarder_thread.start()
    receiver_thread.start()
