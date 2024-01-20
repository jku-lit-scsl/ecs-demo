import asyncio
import json
import logging

import websockets

import config.config as CONFIG
from util.utils import send_update_knowledge_base

host = CONFIG.network_conf['my_ip']

OM = ''
clients = set()
defcon_handler = None


async def handle_msg_receive(websocket, path):
    global clients, defcon_handler
    clients.add(websocket)
    try:
        while True:
            message = await websocket.recv()
            message_obj = json.loads(message)
            if message_obj['defcon_lvl']:
                logging.info(f"Received new message >>> {message_obj}")
                # forward this to the next parent, if possible
                if OM != CONFIG.CLOUD_SERVER:
                    send_update_knowledge_base(defcon_handler, message_obj['defcon_lvl'], message_obj['ip'])
                # check if the clients defcon is more critical than own
                if int(defcon_handler.current_state.id[7]) > int(message_obj['defcon_lvl'][7]):
                    defcon_handler.increase()

            client_response_msg = {
                'defcon_lvl': defcon_handler.current_state.id,
                'ip': host
            }

            # response own defcon level back to clients
            await websocket.send(json.dumps(client_response_msg))
    except websockets.exceptions.ConnectionClosed:
        logging.info("Client disconnected")
    finally:
        clients.remove(websocket)


async def _main_ws_starter():
    server = await websockets.serve(handle_msg_receive, host, 8765)
    logging.info(f"WebSocket server started on ws://{host}:8765")
    await server.wait_closed()


def set_defcon_handler(dc_handler):
    global defcon_handler
    defcon_handler = dc_handler


def start_ws_server(operating_mode):
    global OM, defcon_handler
    while defcon_handler is None:
        pass
    OM = operating_mode
    asyncio.run(_main_ws_starter())
