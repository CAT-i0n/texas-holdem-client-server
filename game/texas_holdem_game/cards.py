from random import shuffle

from pydantic import BaseModel

from .constants import CARD_SUITS, CARD_VALUES


class Card(BaseModel):
    suit: str
    value: int


class Deck:
    def __init__(self):
        self._deck = []
        for suit in CARD_SUITS:
            for value in CARD_VALUES:
                self._deck.append(Card(suit=suit, value=value))
        self._cards = self.reshuffle_deck()

    def reshuffle_deck(self) -> None:
        shuffle(self._deck)
        self._cards = self._deck.copy()

    def get_cards(self, n: int) -> list[Card]:
        n_cards, self._cards = self._cards[:n], self._cards[n:]
        return n_cards
