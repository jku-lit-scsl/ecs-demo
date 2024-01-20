import asyncio
import json
import logging

import websockets

import config.config as CONFIG
from util.utils import send_update_knowledge_base

host = CONFIG.network_conf['my_ip']

OM = ''
clients = set()


async def handle_msg_receive(websocket, path):
    global clients
    clients.add(websocket)
    try:
        while True:
            message = await websocket.recv()
            message_obj = json.loads(message)
            if message_obj['defcon_lvl']:
                logging.info(f"Client >{message_obj['ip']}< switched defcon level to >{message_obj['defcon_lvl']}<")
                if OM != CONFIG.CLOUD_SERVER:
                    send_update_knowledge_base(message_obj['defcon_lvl'], message_obj['ip'])
                # Broadcast to other clients
                await broadcast_defcon_change_to_clients(message_obj)
            await websocket.send(f"Server received: {message}")
    except websockets.exceptions.ConnectionClosed:
        logging.info("Client disconnected")
    finally:
        clients.remove(websocket)


async def broadcast_defcon_change_to_clients(message_obj):
    for client in clients:
        await client.send(
            {
                'adaptation': 'defcon_change',
                'new_defcon': message_obj['defcon_lvl']
            }
        )


async def _main_ws_starter():
    server = await websockets.serve(handle_msg_receive, host, 8765)
    logging.info(f"WebSocket server started on ws://{host}:8765")
    await server.wait_closed()


def start_ws_server(operating_mode):
    global OM
    OM = operating_mode
    asyncio.run(_main_ws_starter())
