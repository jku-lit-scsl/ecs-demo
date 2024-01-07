import asyncio
import logging

import websockets

import config.config as CONFIG

host = CONFIG.network_conf['my_ip']


async def handle_msg_receive(websocket, path):
    try:
        while True:
            message = await websocket.recv()
            print(f"Received message from client: {message}")
            await websocket.send(f"Server received: {message}")
    except websockets.exceptions.ConnectionClosed:
        logging.info("Client disconnected")


async def _main_ws_starter():
    start_server = websockets.serve(handle_msg_receive, host, 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def start_ws_server():
    _main_ws_starter()
