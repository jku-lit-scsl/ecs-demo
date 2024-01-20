from secure_mod.defcon_handler import DefconHandler
from util.mqtt_receiver import set_defcon_handler
from util.setup import setup, get_mqtt_receiver

if __name__ == '__main__':
    setup()
    mqtt_receiver = get_mqtt_receiver()
    defcon_handler = DefconHandler(mqtt_receiver)
    set_defcon_handler(defcon_handler)
    defcon_handler.init_heartbeat()
