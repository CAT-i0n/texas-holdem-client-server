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
    10: "10",
    11: "J",
    12: "Q",
    13: "K",
    14: "A",
}


export function CardImage({ card }) {
    return (<img src={`./data/Deck/${CARD_SUITS[card.suit]}/${CARD_VALUES[card.value]}.png`} />);
}


export function Cards(cards) {
    return (
        <div style={{
            display: 'flex',
            flexDirection: 'row',
            gap: '10px',
            overflowX: 'auto' // Add scroll if images overflow
        }}>
            {cards.map((card) => (
                <CardImage card = {card}/>))}
        </div>
    );
};

export function BackCards() {
    return (<div style={{
        display: 'flex',
        flexDirection: 'row',
        gap: '10px',
        overflowX: 'auto' // Add scroll if images overflow
    }}>
        <img src={`./data/Deck/back.png`} />
        <img src={`./data/Deck/back.png`} />
    </div>)
}