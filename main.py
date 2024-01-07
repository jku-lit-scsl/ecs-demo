import time

from secure_mod.defcon_handler import DefconHandler
from util.setup import setup

if __name__ == '__main__':
    setup()
    defcon_handler = DefconHandler()

    for i in range(3):
        defcon_handler.increase()
        time.sleep(5)
