import { Cards } from "./Cards";
import { WINDOW_RATIO } from "./Consts";
import { CARD_SIZE } from "./Consts";

export function Player({ player, pos }) {
    return (
        <g key={player.name} transform={`translate(${pos.x}, ${pos.y})`}>
            <g transform={`translate(${-CARD_SIZE}, ${-CARD_SIZE*1.55})`}>
            {player.cards && player.cards.length > 0 && (
                <Cards cards={player.cards}/>
            )}
            </g>
            <rect x="-75" y="-25" rx="25" ry="25" width="150" height="50" fill='#432341' stroke={player.is_active ? '#ffffff' : '#444444'} strokeWidth="2" />
            <text y="-3" textAnchor="middle" fill="white" fontSize="15" fontWeight="bold">
                {player.name}
            </text>
            <text y="13" textAnchor="middle" fill="#ffd700" fontSize="14">
                ${player.chips}
            </text>
            {player.bet > 0 && (
                <text y={-90 * Math.sin(pos.angle)-15} x={-90 * WINDOW_RATIO * Math.cos(pos.angle)} textAnchor="middle" fill="#a8a5dc" fontSize="15">
                    ${player.bet}
                </text>
            )}
            {!isNaN(player.role) && (
                <text y={-70 * Math.sin(pos.angle)-15} x={-70 * WINDOW_RATIO * Math.cos(pos.angle)} textAnchor="middle" fill="#ffd700" fontSize="15" fontWeight="bold">
                    {player.role === 0 ? 'D' : player.role === 0.5 ? 'SB' : player.role === 1.0 ? 'BB' : ''}
                </text>
            )}
        </g>
    );
}