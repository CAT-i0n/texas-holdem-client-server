import { Player } from "./player"
import { Cards } from "./cards"


export function Game({ gameState }) {
    const players = gameState.players;
    const board = gameState.cards

    return (<div>
        <div>{players.map((player) => (<Player player={player} />))}</div>

        <div style={{ paddingLeft: '20px' }}>Pot: {gameState.pot}</div>

        <div className="board-cards">
            {board?.length > 0 && Cards(board)}
        </div>
    </div>)
}