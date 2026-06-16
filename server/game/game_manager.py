import asyncio

from .game_client import BaseClient, Bot, CLIClient
from .texas_holdem_game.holdem_game import GameState, PlayerMove, TexasHoldemGame


class GameManager:
    def __init__(self):
        self._clients: dict[str, BaseClient] = {}
        self._game_process = None

    def add_client(self, client: BaseClient):
        if client.name not in self._clients:
            self._clients[client.name] = client
        else:
            raise

    def remove_client(self, name):
        if name in self._clients:
            del self._clients[name]
        if all(isinstance(player, Bot) for player in self._clients):
            self._game_process.cancel()

    def run_game(self):
        """Run the game with all connected clients."""
        if len(self._clients) > 1:
            game = TexasHoldemGame(player_names=[name for name in self._clients])
        else:
            raise

        self._game_process = asyncio.create_task(self.game_loop(game))

    async def game_loop(self, game):
        for game_state in game.game_loop():
            if game_state.active_player:
                player_move = await self._send_state_with_hidden_cards(game_state=game_state)
                game.update_move(move=player_move)
            else:
                # todo: handle exceptions
                async with asyncio.TaskGroup() as tg:
                    for client_name in self._clients:
                        tg.create_task(self._clients[client_name].update_state(game_state))
                await asyncio.sleep(1)

    async def _send_state_with_hidden_cards(self, game_state: GameState) -> PlayerMove:
        """Send the masked game state to all clients and await the active player's move."""
        options = game_state.options.copy()
        state_to_send = game_state.model_copy(update={"options": None})
        client_move = None
        # todo: handle exceptions
        async with asyncio.TaskGroup() as tg:
            for client_name in self._clients:
                # todo mb fix copying
                state_to_send = state_to_send.model_copy()
                players_for_client = [
                    player if player.name == client_name else player.model_copy(update={"cards": []})
                    for player in game_state.players
                ]
                state_to_send.players = players_for_client
                if client_name == state_to_send.active_player:
                    client_move = tg.create_task(
                        self._clients[client_name].move(state_to_send.model_copy(update={"options": options}))
                    )
                else:
                    tg.create_task(self._clients[client_name].update_state(state_to_send))
        return await client_move


if __name__ == "__main__":
    manager = GameManager()
    manager.add_client(CLIClient(name="Player"))
    for i in range(3):
        manager.add_client(Bot(name="Bot" + str(i + 1)))
    asyncio.run(manager.run_game())
