import asyncio
import os
from abc import ABC, abstractmethod

from .texas_holdem_game.constants import CARD_SUITS, CARD_VALUES, PlayerOptions
from .texas_holdem_game.holdem_game import GameState, PlayerMove


class BaseClient(ABC):

    @abstractmethod
    async def move(self, state: GameState) -> PlayerMove:
        pass

    @abstractmethod
    async def update_state(self, state: GameState) -> None:
        pass

    @property
    def name(self) -> str:
        return self._name


class Bot(BaseClient):
    def __init__(self, name):
        self._name = name

    async def move(self, state: GameState):
        # await asyncio.sleep(1)
        if PlayerOptions.CALL in state.options:
            return PlayerMove(move=PlayerOptions.CALL)
        return PlayerMove(move=PlayerOptions.CHECK)

    async def update_state(self, state: GameState) -> None:
        pass


class CLIClient(BaseClient):
    def __init__(self, name):
        self._name = name

    async def move(self, state: GameState) -> PlayerMove:
        await self.update_state(state)
        options = []
        print("options:", end=" ")
        for option in state.options:
            print(option.value, end=" ")
            options.append(option.value)
        print()
        while True:
            option = input("enter move->")
            if option in options:
                match option:
                    case "call":
                        return PlayerMove(move=PlayerOptions.CALL)
                    case "check":
                        return PlayerMove(move=PlayerOptions.CHECK)
                    case "bet":
                        while True:
                            bet = input("enter bet->")
                            bet_range = state.options[PlayerOptions.BET]
                            if bet.isdigit() and bet_range[0] <= int(bet) <= bet_range[1]:
                                return PlayerMove(move=PlayerOptions.BET, bet=int(bet))
                    case "raise":
                        while True:
                            bet = input("enter bet->")
                            bet_range = state.options[PlayerOptions.RAISE]
                            if bet.isdigit() and bet_range[0] <= int(bet) <= bet_range[1]:
                                return PlayerMove(move=PlayerOptions.RAISE, bet=int(bet))
                    case "fold":
                        return PlayerMove(move=PlayerOptions.FOLD)

    async def update_state(self, state: GameState) -> None:
        os.system("clear")
        for player in state.players:
            print(
                f"name: {player.name} {player.role.name if player.role else ""}{" - active" if state.active_player == player.name else ""}\n  chips: {player.chips}\n  bet: {player.bet}"
            )
            if player.cards:
                print(
                    "  cards:",
                    " ".join(CARD_VALUES[card.value] + CARD_SUITS[card.suit] for card in player.cards),
                    player.combination.combination.name if player.combination else "",
                )
            else:
                print("  cards: Xx Xx")
        print("------------------")
        print(" ", " ".join(CARD_VALUES[card.value] + CARD_SUITS[card.suit] for card in state.cards))
        print("------------------")
        print("pot:", state.pot)
        input()
