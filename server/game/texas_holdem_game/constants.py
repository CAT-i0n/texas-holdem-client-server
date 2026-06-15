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


class GameRole(float, Enum):
    BUTTON: int = 0.0
    SMALL_BLIND: int = 0.5
    BIG_BLIND: int = 1.0


class PlayerOptions(str, Enum):
    BET: str = "bet"
    CHECK: str = "check"
    FOLD: str = "fold"
    CALL: str = "call"
    RAISE: str = "raise"


class Combinations(Enum):
    HIGH_CARD: int = 0
    PAIR: int = 1
    TWO_PAIRS: int = 2
    THREE_OF_A_KING: int = 3
    STRAIGHT: int = 4
    FLUSH: int = 5
    FULL_HOUSE: int = 6
    FOUR_OF_A_KING: int = 7
    STRAIGHT_FLUSH: int = 8
    ROYAL_FLUSH: int = 9


FISRT_PLAYER_NUM = "first_player_num"
CARDS_TO_BOARD = "cards_to_boards"

GAME_ROUNDS = (
    {FISRT_PLAYER_NUM: 3, CARDS_TO_BOARD: 0},
    {FISRT_PLAYER_NUM: 1, CARDS_TO_BOARD: 3},
    {FISRT_PLAYER_NUM: 1, CARDS_TO_BOARD: 1},
    {FISRT_PLAYER_NUM: 1, CARDS_TO_BOARD: 1},
)
