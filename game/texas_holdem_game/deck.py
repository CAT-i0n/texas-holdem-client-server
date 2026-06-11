from random import shuffle

from .constants import CARD_SUITS, CARD_VALUES
from .models import Card


class Deck:
    def __init__(self):
        self._deck = []
        for suit in CARD_SUITS:
            for value in CARD_VALUES:
                self._deck.append(Card(suit=suit, value=value))
        self._cards = self.reshuffle_deck()

    def reshuffle_deck(self) -> None:
        """Regenerate and reshuffle the deck."""
        shuffle(self._deck)
        self._cards = self._deck.copy()

    def get_cards(self, n: int) -> list[Card]:
        """Deal n cards from the deck."""
        n_cards, self._cards = self._cards[:n], self._cards[n:]
        return n_cards
