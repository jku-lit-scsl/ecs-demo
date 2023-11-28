from util.mqtt_forwarder import MQTTForwarder
from util.utils import get_current_time_in_millis, setup

if __name__ == '__main__':
    setup()
    mqtt_fw = MQTTForwarder()
    mqtt_fw.publish("python/test", f"{get_current_time_in_millis()}")
