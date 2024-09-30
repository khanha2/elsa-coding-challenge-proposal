import json
import os

import asyncio

from typing import Dict, List
from starlette.websockets import WebSocket

from aio_pika import connect, Message, IncomingMessage


class Notifier:

    def __init__(self):
        self.quiz_connection_map: Dict[int, List[WebSocket]] = {}
        self.is_ready = False

    async def start(self):
        if self.is_ready:
            return

        self.rmq_conn = await connect(
            os.environ.get('RABBITMQ_URL'),
            loop=asyncio.get_running_loop()
        )
        self.channel = await self.rmq_conn.channel()
        queue = await self.channel.declare_queue("message_broadcasting",  durable=True)
        await queue.consume(self._notify, no_ack=True)
        self.is_ready = True

    async def connect(self, websocket: WebSocket, quiz_id: int):
        await websocket.accept()
        connections = self.quiz_connection_map.get(quiz_id, [])
        connections.append(websocket)
        self.quiz_connection_map[quiz_id] = connections

    def remove(self, websocket: WebSocket, quiz_id: int):
        connections = self.quiz_connection_map.get(quiz_id, [])
        connections.remove(websocket)
        self.quiz_connection_map[quiz_id] = connections

    def _notify(self, message: IncomingMessage):
        message_text = message.body
        message_dict = json.loads(message_text)
        print(message_dict)

        quiz_id = message_dict['quiz_id']
        connections = self.quiz_connection_map.get(quiz_id, [])
        for connection in connections:
            asyncio.create_task(connection.send_text(message_text))

