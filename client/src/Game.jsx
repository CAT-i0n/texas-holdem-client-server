import { Table } from "./Table";
import { VIEW_BOX_SIZE } from "./Consts";
import { OptionButtons } from "./OptionButtons";

export function Game({ gameState, playerName, send_data }) {
    let players = gameState.players;
    const board = gameState.cards

    const index = players.findIndex(u => u.name === playerName)
    players = [...players.slice(index), ...players.slice(0, index)]


    return (<div className="table-container">
        <svg viewBox={`0 0 ${VIEW_BOX_SIZE.x} ${VIEW_BOX_SIZE.y}`}
            preserveAspectRatio="xMidYMid slice"
            className="poker-table-svg"
        >
            <Table players={players} board={board} pot={gameState.pot} />
            {gameState.options && <OptionButtons options={gameState.options} send_data={send_data} />}
        </svg>
    </div>)
}