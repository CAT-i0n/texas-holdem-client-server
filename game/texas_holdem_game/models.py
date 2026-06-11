from pydantic import BaseModel

from typing import Union
from .deck import Card
from .constants import PlayerOptions, Combinations

ActionValue = Union[None, int, tuple[int, int]]


class GameState(BaseModel):
    players: list[Player]
    pot: int
    cards: list[Card] = []
    active_player: str | None = None
    options: dict[PlayerOptions, ActionValue] = {}


class PlayerMove(BaseModel):
    move: PlayerOptions
    bet: int | None = None


class Player(BaseModel):
    name: str
    chips: int = 0
    bet: int = 0
    cards: list[Card] = []
    is_active: bool = True
    # combination: Combination | None = None

    def bet_chips(self, bet):
        if self.bet + self.chips > bet:
            diff = bet - self.bet
            self.chips -= diff
            self.bet = bet
        else:
            self.bet = bet
            self.chips = 0

    def __hash__(self):
        return hash(self.name)


class Combination(BaseModel):
    combination: Combinations
    cards: list[Card]
    top_values: tuple[int, ...]

    def __gt__(self, other: Combination):
        return (self.combination.value, self.top_values) > (other.combination.value, other.top_values)

    def __eq__(self, other: Combination):
        return (self.combination.value, self.top_values) == (other.combination.value, other.top_values)

    def __hash__(self):
        return hash((self.combination.value, self.top_values))


class Card(BaseModel):
    suit: str
    value: int
