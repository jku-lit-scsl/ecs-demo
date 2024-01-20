import asyncio
import json

import websockets

import config.config as CONFIG

host = CONFIG.network_conf['server_ip']


async def _send_msg_ws(message, defcon_handler):
    uri = f"ws://{host}:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        response_obj = json.loads(response)
        # if parent's defcon is greate than own, increase own defcon lvl
        if response_obj['defcon_lvl'] and int(defcon_handler.current_state.id[7]) > int(response_obj['defcon_lvl'][7]):
            defcon_handler.increase()


def send_msg_websocket(msg, defcon_handler):
    asyncio.run(_send_msg_ws(msg, defcon_handler))
