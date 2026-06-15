from collections import Counter
from itertools import groupby, permutations

from .constants import Combinations
from .deck import Card
from .models import Card, Combination, Player


class CombinationComparator:

    def get_winners(self, players: list[Player], board_cards: list[Card]) -> list[list[Player]]:
        """Compute each player's best hand combination and return groups of players sorted by hand strength."""
        for player in players:
            player.combination = self._get_best_combination(player.cards + board_cards)

        players = sorted(players, key=lambda player: player.combination, reverse=True)
        return [list(group) for _, group in groupby(players, key=lambda player: player.combination)]

    def _get_best_combination(self, cards: list[Card]) -> Combination:
        """Compute the best 5-card hand combination from a list of cards."""
        combinations: list[Combination] = []
        for hand in permutations(cards, 5):
            combinations.append(self._compute_combination(hand))
        return max(combinations)

    def _compute_combination(self, hand: list[Card]) -> Combination:
        top_values = sorted(Counter(card.value for card in hand).most_common(), key=lambda x: (-x[1], -x[0]))
        top_cards = tuple(value for value, _ in top_values)
        if top_values[0][1] == 2:
            combination = Combinations.TWO_PAIRS if top_values[1][1] == 2 else Combinations.PAIR
        elif top_values[0][1] == 3:
            combination = Combinations.FULL_HOUSE if top_values[1][1] == 2 else Combinations.THREE_OF_A_KING
        elif self._is_straight(top_cards):
            if self._is_flush(hand):
                combination = (
                    Combinations.ROYAL_FLUSH if top_cards == (14, 13, 12, 11, 10) else Combinations.STRAIGHT_FLUSH
                )
            else:
                combination = Combinations.STRAIGHT
        elif self._is_flush(hand):
            combination = Combinations.FLUSH
        elif top_values[0][1] == 4:
            combination = Combinations.FOUR_OF_A_KING
        else:
            combination = Combinations.HIGH_CARD
        return Combination(
            combination=combination,
            cards=hand,
            top_values=top_cards if top_cards != (14, 5, 4, 3, 2) else (1, 2, 3, 4, 5),
        )

    def _is_flush(self, hand: list[Card]):
        return len(set(card.suit for card in hand)) == 1

    def _is_straight(self, values: list[int]):
        return len(values) == 5 and (values[0] - values[4] == 4 or values == (14, 5, 4, 3, 2))


# if __name__ == "__main__":
#     c = CombinationComparator()
#     player1 = Player(
#         name="a",
#         cards=[
#             Card(suit="h", value=14),
#             Card(suit="d", value=5),
#         ],
#     )
#     player2 = Player(
#         name="b",
#         cards=[
#             Card(suit="s", value=14),
#             Card(suit="c", value=10),
#         ],
#     )
#     winners = c.get_winners(
#         players=[player1, player2],
#         board_cards=[
#             Card(suit="h", value=14),
#             Card(suit="d", value=5),
#             Card(suit="c", value=3),
#             Card(suit="h", value=6),
#             Card(suit="c", value=7),
#         ],
#     )
#     for item in winners:
#         print(item)
