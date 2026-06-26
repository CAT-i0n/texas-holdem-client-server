import asyncio
from asyncio import CancelledError, Task
from json import JSONDecodeError

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketState

from .game.game_manager import BaseClient, Bot, GameManager, GameState, NotEnoughPlayersException, PlayerMove
from .game.texas_holdem_game.constants import PlayerOptions


class WebSocketClient(BaseClient):
    def __init__(self, name, websocket: WebSocket):
        self._name = name
        self._websocket = websocket
        # todo: property
        self.wait_task: Task | None = None

    async def move(self, state: GameState) -> PlayerMove:
        await self.update_state(state=state)
        try:
            player_move = await self.wait_task
            move = PlayerMove.model_validate_json(player_move)
            return move
        except WebSocketDisconnect, CancelledError:
            return PlayerMove(move=PlayerOptions.FOLD)

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
            if not self.game_manager.is_game_running():
                try:
                    await self.game_manager.run_game()
                except NotEnoughPlayersException as e:
                    pass

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
                    except CancelledError:
                        pass
            except WebSocketDisconnect:
                self.game_manager.remove_client(name)
            except Exception as e:
                print(f"WebSocket connection closed with exception: {e}")


server = GameServer(bots_number=0)
app = server.app
