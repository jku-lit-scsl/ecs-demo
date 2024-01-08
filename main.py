import time

from secure_mod.defcon_handler import DefconHandler
from util.setup import setup, get_mqtt_receiver

if __name__ == '__main__':
    setup()
    mqtt_receiver = get_mqtt_receiver()
    defcon_handler = DefconHandler(mqtt_receiver)

    for i in range(3):
        defcon_handler.increase()
        time.sleep(5)
