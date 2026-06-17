import asyncio
from json import JSONDecodeError
from typing import Coroutine

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from .game.game_manager import BaseClient, Bot, GameManager, GameState, PlayerMove
from .game.texas_holdem_game.constants import PlayerOptions

from starlette.websockets import WebSocketState


class WebSocketClient(BaseClient):
    def __init__(self, name, websocket: WebSocket):
        self._name = name
        self._websocket = websocket
        # todo: property
        self.wait_task: Coroutine = None

    async def move(self, state: GameState) -> PlayerMove:
        await self.update_state(state=state)
        while True:
            player_move = await self.wait_task
            try:
                move = PlayerMove.model_validate_json(player_move)
                return move
            except JSONDecodeError, ValidationError:
                pass

    async def update_state(self, state: GameState) -> None:
        if self._websocket.client_state == WebSocketState.CONNECTED:
            await self._websocket.send_json(state.model_dump())


class GameServer:
    def __init__(self, bots_number: int = 0):
        self.game_manager = GameManager()
        for i in range(bots_number):
            self.game_manager.add_client(Bot(name="Bot" + str(i + 1)))
        self.app = FastAPI()

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/start")
        async def start_game():
            self.game_manager.run_game()

        @self.app.websocket("/connect/{name}")
        async def connect_player(websocket: WebSocket, name: str):
            try:
                client = WebSocketClient(name=name, websocket=websocket)
                self.game_manager.add_client(client)
                await websocket.accept()
                while True:
                    task_message = asyncio.create_task(websocket.receive_text())
                    client.wait_task = task_message
                    try:
                        await task_message
                    except JSONDecodeError:
                        continue
            except WebSocketDisconnect:
                pass
            except Exception as e:
                print(f"WebSocket connection closed with exception: {e}")
            finally:
                self.game_manager.remove_client(name)


server = GameServer(bots_number=2)
app = server.app
