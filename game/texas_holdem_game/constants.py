from enum import Enum

CARD_SUITS = {"spades": "S", "hearts": "H", "diamonds": "D", "clubs": "C"}
CARD_VALUES = {
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "J",
    12: "Q",
    13: "K",
    14: "A",
}

CHIPS_TO_BLIND_RATIO = 100


class GameRole(Enum):
    BUTTON = 0
    SMALL_BLIND = 0.5
    BIG_BLIND = 1


class PlayerOptions(Enum):
    BET = "bet"
    CHECK = "check"
    FOLD = "fold"
    CALL = "call"
    RAISE = "raise"


class Combinations(Enum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_A_KING = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KING = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9


FISRT_PLAYER_NUM = "first_player_num"
CARDS_TO_BOARD = "cards_to_boards"

GAME_ROUNDS = (
    {FISRT_PLAYER_NUM: 3, CARDS_TO_BOARD: 0},
    {FISRT_PLAYER_NUM: 1, CARDS_TO_BOARD: 3},
    {FISRT_PLAYER_NUM: 1, CARDS_TO_BOARD: 1},
    {FISRT_PLAYER_NUM: 1, CARDS_TO_BOARD: 1},
)
