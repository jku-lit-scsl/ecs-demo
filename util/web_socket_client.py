import asyncio

import websockets

import config.config as CONFIG

host = CONFIG.network_conf['server_ip']


async def connect():
    uri = f"ws://{host}:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = f"This message comes from the following client IP address{CONFIG.network_conf['my_ip']}"
            await websocket.send(message)
            response = await websocket.recv()
            print(f"Received from server: {response}")


def start_ws_client():
    asyncio.run(connect())
