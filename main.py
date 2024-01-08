from secure_mod.defcon_handler import DefconHandler
from util.mqtt_receiver import set_defcon_handler
from util.setup import setup

if __name__ == '__main__':
    setup()
    defcon_handler = DefconHandler()
    set_defcon_handler(defcon_handler)
