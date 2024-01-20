import logging

from secure_mod.defcon_handler import DefconHandler
from util.mqtt_receiver import set_defcon_handler
from util.setup import setup, get_mqtt_receiver


def setup_logging():
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.getLogger().setLevel(logging.INFO)


if __name__ == '__main__':
    setup_logging()
    setup()
    mqtt_receiver = get_mqtt_receiver()
    defcon_handler = DefconHandler(mqtt_receiver)
    set_defcon_handler(defcon_handler)
    defcon_handler.init_heartbeat()
