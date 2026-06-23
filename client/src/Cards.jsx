const CARD_SUITS = { "spades": "S", "hearts": "H", "diamonds": "D", "clubs": "C" }
const CARD_VALUES = {
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "T",
    11: "J",
    12: "Q",
    13: "K",
    14: "A",
}
import { CARD_SIZE } from "./Consts"


export function Cards({ cards }) {
    return <g>
        {cards.map((card, cardIndex) => (
            <g key={cardIndex} transform={`translate(${cardIndex * CARD_SIZE}, 0)`}>
                {card ? <image href={`./assets/Deck/${CARD_VALUES[card.value]}${CARD_SUITS[card.suit]}.svg`} width={CARD_SIZE} />
                    : <image href={`./assets/Deck/2B.svg`} width={CARD_SIZE} />}
            </g>
        ))}
    </g>
};
