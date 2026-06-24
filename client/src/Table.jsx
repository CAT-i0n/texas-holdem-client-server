import { Player } from "./Player";
import { Cards } from "./Cards";
import { VIEW_BOX_SIZE, CENTER_COORDS, TABLE_PARAMS, CARD_SIZE } from "./Consts";

export function Table({ players, board, pot }) {
    const getPlayerPositions = (count) => {
        const positions = [];

        for (let i = 0; i < count; i++) {
            const angle = (i / count) * 2 * Math.PI + Math.PI / 2;

            positions.push({
                x: CENTER_COORDS.x + (TABLE_PARAMS.x+10) * Math.cos(angle),
                y: CENTER_COORDS.y + (TABLE_PARAMS.y+10) * Math.sin(angle),
                angle: angle
            });
        }

        return positions;
    };

    const positions = getPlayerPositions(players.length);

    return (
        <g>
            <ellipse
                cx={CENTER_COORDS.x}
                cy={CENTER_COORDS.y}
                rx={TABLE_PARAMS.x}
                ry={TABLE_PARAMS.y}
                fill="#8f1616" stroke="black" strokeWidth="2"
            />
            <ellipse
                cx={CENTER_COORDS.x}
                cy={CENTER_COORDS.y}
                rx={TABLE_PARAMS.x - 25}
                ry={TABLE_PARAMS.y - 20}
                fill="green" stroke="black" strokeWidth="2"
            />
            {players.map((player, index) => (
                <Player player={player} pos={positions[index]} />
            ))}
            <g transform={`translate(${CENTER_COORDS.x - CARD_SIZE*2.5}, ${CENTER_COORDS.y - 35})`}>
                <Cards cards={board} />
            </g>
            <text y={CENTER_COORDS.y - 40} x={CENTER_COORDS.x} textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">
                ${pot}
            </text>
        </g>
    );
}