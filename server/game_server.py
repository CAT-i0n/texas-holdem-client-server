import asyncio
from json import JSONDecodeError
from typing import Coroutine

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from .game.game_manager import BaseClient, Bot, GameManager, GameState, PlayerMove


class WebSocketClient(BaseClient):
    def __init__(self, name, websocket: WebSocket):
        self._name = name
        self._websocket = websocket
        # todo: property
        self.wait_task: Coroutine = None

    async def move(self, state: GameState) -> PlayerMove:
        await self.update_state(state=state)
        while True:
            try:
                player_move = await self.wait_task
                return PlayerMove.model_validate_json(player_move)
            except ValidationError, JSONDecodeError:
                pass

    async def update_state(self, state: GameState) -> None:
        await self._websocket.send_json(state.model_dump())


class GameServer:
    def __init__(self):
        self.game_manager = GameManager()
        for i in range(3):
            self.game_manager.add_client(Bot(name="Bot" + str(i + 1)))
        self.app = FastAPI()
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/start")
        async def start_game():
            await self.game_manager.run_game()

        @self.app.websocket("/connect/{name}")
        async def connect_player(websocket: WebSocket, name: str):
            try:
                client = WebSocketClient(name=name, websocket=websocket)
                self.game_manager.add_client(client)
                await websocket.accept()
                print("opened")
                while True:
                    task_message = asyncio.create_task(websocket.receive_json())
                    client.wait_task = task_message
                    try:
                        await task_message
                    except JSONDecodeError:
                        continue
            except WebSocketDisconnect:
                print("closed")
            except Exception as e:
                print(f"WebSocket connection closed with exception: {e}")
            finally:
                self.game_manager.remove_client(name)


server = GameServer()
app = server.app
