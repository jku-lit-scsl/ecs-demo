import threading
import time

from secure_mod.defcon_handler import DefconHandler
from util.setup import setup
from util.web_socket_client import send_msg_websocket

if __name__ == '__main__':
    setup()
    defcon_handler = DefconHandler()

    for i in range(10):
        threading.Thread(target=send_msg_websocket).start()
        time.sleep(3)
