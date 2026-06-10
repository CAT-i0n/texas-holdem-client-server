from pydantic import BaseModel

from .cards import Card


class Player(BaseModel):
    name: str
    chips: int = 0
    bet: int = 0
    cards: list[Card] = []
    is_active: bool = True

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
