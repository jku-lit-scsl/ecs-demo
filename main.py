import time

from secure_mod.defcon_handler import DefconHandler
from util.mqtt_receiver import set_defcon_handler
from util.setup import setup, get_mqtt_receiver

if __name__ == '__main__':
    setup()
    mqtt_receiver = get_mqtt_receiver()
    defcon_handler = DefconHandler()
    set_defcon_handler(defcon_handler)

    for i in range(3):
        defcon_handler.increase()
        time.sleep(5)
