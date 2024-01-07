import asyncio
import json
import logging

import websockets

import config.config as CONFIG
from util.utils import send_update_knowledge_base

host = CONFIG.network_conf['my_ip']


async def handle_msg_receive(websocket, path):
    try:
        while True:
            message = await websocket.recv()
            message_obj = json.loads(message)
            if message_obj['defcon_lvl']:
                logging.info(f"Client >{message_obj['ip']}<switched defcon level to {message_obj['defcon_lvl']}")
                send_update_knowledge_base(message_obj['defcon_lvl'], message_obj['ip'])
            # todo: change behavior?
            # todo: forward to next parent
            await websocket.send(f"Server received: {message}")
    except websockets.exceptions.ConnectionClosed:
        logging.info("Client disconnected")


async def _main_ws_starter():
    server = await websockets.serve(handle_msg_receive, host, 8765)

    logging.info(f"WebSocket server started on ws://{host}:8765")

    await server.wait_closed()


def start_ws_server():
    asyncio.run(_main_ws_starter())
