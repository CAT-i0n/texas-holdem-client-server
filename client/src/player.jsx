import { Cards, BackCards } from "/src/cards"

export function Player({ player }) {
    return (
        <div className={`player ${player.is_active ? 'active' : 'folded'}`}>
            <div className="player-info">
                <span className="player-name">{player.name}</span>
                {" "}
                {player.combination && (
                <span className="player-name">{player.combination.combination}</span>)}
            </div>

            <div style={{ paddingLeft: '20px' }}>Bet: {player.bet > 0 && player.bet}</div>
            <div style={{ paddingLeft: '20px' }}>Chips: {player.chips > 0 && player.chips}</div>

            <div className="player-cards">
                {player.cards?.length > 0 ?
                    Cards(player.cards) :
                    BackCards()
                }
            </div>
        </div>
    );
}