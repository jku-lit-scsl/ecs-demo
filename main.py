from secure_mod.defcon_handler import DefconHandler
from util.mqtt_forwarder import MQTTForwarder
from util.setup import setup

if __name__ == '__main__':
    mqtt_fw = MQTTForwarder()
    setup(mqtt_fw)
    # mqtt_fw.publish("python/test", f"{get_current_time_in_millis()}")
    #
    defcon_handler = DefconHandler(mqtt_fw)
    #
    # time.sleep(6)
    # defcon_handler.increase()

