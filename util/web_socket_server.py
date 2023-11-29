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
    server = await websockets.serve(handle_msg_receive, host, 8765)

    print(f"WebSocket server started on ws://{host}:8765")

    await server.wait_closed()


def start_ws_server():
    asyncio.run(_main_ws_starter())
