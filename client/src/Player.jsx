import { Cards } from "./Cards";
import { WINDOW_RATIO } from "./Consts";

export function Player({ player, pos }) {
    return (
        <g key={player.name} transform={`translate(${pos.x}, ${pos.y})`}>
            <g transform="translate(-40, -60)">
            {player.cards && player.cards.length > 0 && (
                <Cards cards={player.cards}/>
            )}
            </g>
            <rect x="-60" y="-20" rx="20" ry="20" width="120" height="40" fill='#432341' stroke={player.is_active ? '#ffffff' : '#444444'} strokeWidth="2" />
            <text y="-3" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">
                {player.name}
            </text>
            <text y="10" textAnchor="middle" fill="#ffd700" fontSize="11">
                ${player.chips}
            </text>
            {player.bet > 0 && (
                <text y={-70 * Math.sin(pos.angle)-15} x={-70 * WINDOW_RATIO * Math.cos(pos.angle)} textAnchor="middle" fill="#a8a5dc" fontSize="10">
                    ${player.bet}
                </text>
            )}
            {!isNaN(player.role) && (
                <text y={-55 * Math.sin(pos.angle)-15} x={-55 * WINDOW_RATIO * Math.cos(pos.angle)} textAnchor="middle" fill="#ffd700" fontSize="10" fontWeight="bold">
                    {player.role === 0 ? 'D' : player.role === 0.5 ? 'SB' : player.role === 1.0 ? 'BB' : ''}
                </text>
            )}
        </g>
    );
}