from contextlib import asynccontextmanager
import asyncio

from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import HTMLResponse
from .notifier import Notifier

notifier = Notifier()

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>coreboard Test</title>
    </head>
    <body>
        <h1>Scoreboard Test</h1>
        <form action="" onsubmit="connectWS1(event)">
            <button>Connect to ws://localhost:8001/quizzes/{quiz_id}/ws</button>
        </form>
        <ul id='messages'></ul>
        <script>
            function connectWS1(event) {
                var ws = new WebSocket("ws://localhost:8001/quizzes/{quiz_id}/ws");
                ws.addEventListener('open', (event) => {
                    alert('WebSocket Connected!')
                });
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/{quiz_id}")
async def get(quiz_id: int):
    response_html = html.replace("{quiz_id}", str(quiz_id))
    return HTMLResponse(response_html)


@app.websocket("/quizzes/{quiz_id}/ws")
async def websocket_endpoint(*, websocket: WebSocket, quiz_id: int):
    await notifier.start()
    await notifier.connect(websocket, quiz_id)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        notifier.remove(websocket)
