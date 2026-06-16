from collections import defaultdict, deque
from itertools import cycle
from typing import Generator

from .combination_comparator import CombinationComparator
from .constants import CARDS_TO_BOARD, CHIPS_TO_BLIND_RATIO, FISRT_PLAYER_NUM, GAME_ROUNDS, GameRole, PlayerOptions
from .deck import Card, Deck
from .models import ActionValue, Card, GameState, Player, PlayerMove


class TexasHoldemGame:
    """A Texas Hold'em poker game engine.

    Manages players, chips, betting rounds, and hand evaluation.
    The main entry point is the game_loop() generator, which yields
    GameState objects after each player action.
    """

    def __init__(self, player_names: list[str], blind_size: int = 10, deck=Deck()):
        self._players: list[Player] = [Player(name=name) for name in player_names]
        self._blind_size: int = blind_size
        self._deck: Deck = deck
        self._pot: dict[Player, int] = defaultdict(int)
        self._current_bet: int = 0
        self._board_cards: list[Card] = []
        self._active_player: Player | None = None
        self._current_order: deque[Player] = []
        self._combination_comparator = CombinationComparator()

    def _playing_order_generator(self) -> Generator[list[Player]]:
        """Generate the playing orderfor for each deal."""
        order = []
        for player in cycle(self._players):
            if order and player == order[0]:
                yield order
                order = []
                continue
            if player.is_active:
                order.append(player)

    def _current_order_generator(self, player: Player) -> deque[Player]:
        """Generate the playing order for the current round."""
        ind = self._players.index(player)
        order = deque()
        for player in self._players[ind:] + self._players[:ind]:
            if player.cards:
                order.append(player)
        return order if len(order) >= 2 else deque()

    def _gen_state(
        self,
        active_player: Player | None = None,
        options: dict[PlayerOptions, ActionValue] = {},
    ) -> GameState:
        """Generate the current state of the game."""
        self._active_player = active_player
        state = GameState(
            players=self._players,
            pot=sum(self._pot.values()),
            cards=self._board_cards,
            active_player=active_player.name if active_player else None,
            options=options,
        )
        return state

    def _gen_options(self, player: Player) -> dict[PlayerOptions, ActionValue]:
        """Generate available moves for the player."""
        options = {}
        if player.chips > 0:
            options[PlayerOptions.FOLD] = None
            if player.bet < self._current_bet:
                options[PlayerOptions.CALL] = min(player.chips, self._current_bet - player.bet)
                if self._current_bet and player.chips + player.bet > self._current_bet * 2:
                    options[PlayerOptions.RAISE] = (min(player.chips, self._current_bet * 2), player.chips)
            else:
                options[PlayerOptions.CHECK] = None
                options[PlayerOptions.BET] = (min(player.chips, self._blind_size), player.chips)
        return options

    def update_move(self, move: PlayerMove) -> None:
        """Update the game state based on the player's move."""
        match move.move:
            case PlayerOptions.FOLD:
                self._pot[self._active_player] += self._active_player.bet
                self._active_player.cards.clear()
            case PlayerOptions.CALL:
                self._active_player.bet_chips(self._current_bet)
            case PlayerOptions.BET | PlayerOptions.RAISE:
                self._current_bet = move.bet
                self._active_player.bet_chips(move.bet)
                self._current_order.clear()
                self._current_order = self._current_order_generator(self._active_player)
                self._current_order.popleft()

    def game_loop(self) -> Generator[GameState]:
        """Run the main game loop and yield the game state after each action."""
        for player in self._players:
            player.chips = self._blind_size * CHIPS_TO_BLIND_RATIO

        order_generator = self._playing_order_generator()
        while sum(player.is_active for player in self._players) > 1:

            # initiate round
            players_order = next(order_generator)
            self._set_roles(players_order)
            self._deck.reshuffle_deck()
            for player in players_order:
                player.cards = self._deck.get_cards(2)

            # game
            for round in GAME_ROUNDS:
                yield from self._betting_round(
                    first_player=players_order[round[FISRT_PLAYER_NUM] % len(players_order)],
                    cards_to_board=round[CARDS_TO_BOARD],
                )
                active_players = [player for player in self._players if player.cards]
                if len(active_players) == 1:
                    active_players[0].chips += sum(self._pot.values())
                    break

            # showdown
            yield from self._end_deal()

        yield self._gen_state()

    def _end_deal(self):
        """Compute winners, yield the final game state, and clear the deal data."""
        active_players = [player for player in self._players if player.cards]
        if len(active_players) > 1:
            winners = self._combination_comparator.get_winners(active_players, self._board_cards)
            yield self._gen_state()
            self._compute_result(winners=winners)

        self._board_cards.clear()
        self._pot.clear()
        for player in active_players:
            player.combination = None
            player.cards.clear()
        for player in self._players:
            if player.chips == 0:
                player.is_active = False
            player.role = None

    def _set_roles(self, playing_order: list[Player]):
        """Set the button, small blind, and big blind roles."""
        for player, role in zip(cycle(playing_order), GameRole):
            player.role = role
            player.bet_chips(min(int(self._blind_size * role.value), player.chips))
        self._current_bet = self._blind_size

    def _betting_round(self, first_player: Player, cards_to_board: int = 0) -> Generator[GameState]:
        """Yield game states during a betting round."""
        self._board_cards += self._deck.get_cards(cards_to_board)
        self._current_order = self._current_order_generator(first_player)
        while self._current_order:
            player = self._current_order.popleft()
            options = self._gen_options(player)
            if options:
                yield self._gen_state(
                    active_player=player,
                    options=options,
                )
        self._current_bet = 0
        for player in self._players:
            self._pot[player] += player.bet
            player.bet = 0
        return

    def _compute_result(self, winners: list[list[Player]]) -> None:
        """Distribute the pot and compute the winning amounts for each player."""
        pot = sum(self._pot.values())
        active_players = sorted(
            [player for player in self._players if player.cards],
            key=lambda player: self._pot[player],
        )

        side_pots = {}
        pot_sums = 0
        min_bet = 0
        for ind, player in enumerate(active_players):
            if not pot:
                break
            win = min(sum(min(value, self._pot[player]) for value in list(self._pot.values())) - pot_sums, pot)
            if self._pot[player] > min_bet:
                side_pots[win] = active_players[ind:]
                min_bet = self._pot[player]
                pot -= win
                pot_sums += win

        for side_amount, eligible_list in list(side_pots.items()):
            for players_in_group in winners:
                actual_winners = [p for p in players_in_group if p in eligible_list]
                if actual_winners:
                    share = side_amount // len(actual_winners)
                    remainder = side_amount % len(actual_winners)
                    for p in actual_winners:
                        p.chips += share
                    if remainder:
                        actual_winners[0].chips += remainder
                    break
