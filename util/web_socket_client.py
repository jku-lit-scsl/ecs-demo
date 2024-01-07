import asyncio

import websockets

import config.config as CONFIG

host = CONFIG.network_conf['server_ip']


async def _send_msg_ws(
        message=f"This message comes from the following client IP address{CONFIG.network_conf['my_ip']}"):
    uri = f"ws://{host}:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        print(f"Received from server: {response}")


def send_msg_websocket(msg):
    asyncio.run(_send_msg_ws(msg))
