import asyncio
from asyncio import CancelledError, Task

from .game_client import BaseClient, Bot, CLIClient
from .texas_holdem_game.holdem_game import GameState, PlayerMove, TexasHoldemGame, PlayerOptions


class NotEnoughPlayersException(Exception):
    def __init__(self):
        super().__init__("Not ennough players to start")


class GameManager:
    def __init__(self):
        self._clients: dict[str, BaseClient] = {}
        self._game_process: Task | None = None
        self._game: TexasHoldemGame | None = TexasHoldemGame(player_names=[name for name in self._clients])
        self._wait_player_move: Task | None = None

    def is_game_running(self) -> bool:
        return bool(self._game_process)

    def _send_current_state(self):
        asyncio.create_task(
            self._send_state_with_hidden_cards(game_state=self._game.get_current_state(), await_move=False)
        )

    def add_client(self, client: BaseClient):
        if client.name not in self._clients:
            self._clients[client.name] = client
            self._game.add_player(client.name)
            if self._game_process:
                self._send_current_state()
        else:
            raise

    def remove_client(self, name):
        if name in self._clients:
            del self._clients[name]
            active_players_num = self._game.remove_player(name)
            self._send_current_state()
        if all(isinstance(player, Bot) for player in self._clients) or len(self._clients) == 1:
            if self._game_process:
                self._game_process.cancel()
            if active_players_num == 1:
                self._game.reset()
                if self._wait_player_move:
                    self._wait_player_move.cancel()
            self._send_current_state()

    async def run_game(self):
        """Run the game with all connected clients."""
        if len(self._clients) > 1:
            try:
                self._game_process = asyncio.create_task(self.game_loop())
                await self._game_process
            except CancelledError:
                self._game_process = None
        else:
            raise NotEnoughPlayersException

    async def game_loop(self):
        for game_state in self._game.game_loop():
            if game_state.active_player:
                try:
                    player_move = await self._send_state_with_hidden_cards(game_state=game_state)
                except CancelledError:
                    if len(self._clients) == 1:
                        raise CancelledError
                else:
                    if player_move:
                        self._game.update_move(move=player_move)
                finally:
                    self._wait_player_move = None
            else:
                # todo: handle exceptions
                async with asyncio.TaskGroup() as tg:
                    for client_name in self._clients:
                        tg.create_task(self._clients[client_name].update_state(game_state))
                await asyncio.sleep(5)

    async def _send_state_with_hidden_cards(self, game_state: GameState, await_move: bool = True) -> Task | None:
        """Send the masked game state to all clients and await the active player's move."""
        options = game_state.options.copy()
        state_to_send = game_state.model_copy(update={"options": None})
        # todo: handle exceptions
        async with asyncio.TaskGroup() as tg:
            for client_name in self._clients:
                # todo mb fix copying
                state_to_send = state_to_send.model_copy()
                players_for_client = [
                    (
                        player
                        if player.name == client_name
                        else (
                            player.model_copy(update={"cards": [None, None]})
                            if player.cards
                            else player.model_copy(update={"cards": []})
                        )
                    )
                    for player in game_state.players
                ]
                state_to_send.players = players_for_client
                if client_name == state_to_send.active_player:
                    active_player_state = state_to_send.model_copy(update={"options": options})
                    if await_move:
                        self._wait_player_move = tg.create_task(self._clients[client_name].move(active_player_state))
                    else:
                        tg.create_task(self._clients[client_name].update_state(active_player_state))
                else:
                    tg.create_task(self._clients[client_name].update_state(state_to_send))
        return await self._wait_player_move if self._wait_player_move else None
