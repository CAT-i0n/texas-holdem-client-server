import { createRoot } from "react-dom/client";
import { Game } from "./src/Game";
import { OptionButtons } from "./src/OptionButtons"

const startEndpoint = `/start`

const wsProtocol = location.protocol === 'https:' ? 'wss' : 'ws';
const ws = new WebSocket(`${wsProtocol}://${location.host}/connect/Player${String(Date.now()).slice(-4, -1)}`);


function send_data(move, bet = NaN) {
    ws.send(JSON.stringify({ "move": move, "bet": bet }))
}

ws.onopen = () => {
    console.log('Connected to WebSocket server');
};
ws.onmessage = (event) => {
    const gameState = JSON.parse(event.data)
    root.render(<div>
        <Game gameState={gameState} />
        {
            gameState?.options &&
            <OptionButtons options={gameState.options} send_data={send_data} />
        }
    </div>
    )
};
ws.onclose = () => {
    console.log('Connection closed');
};
ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};

async function start_game() {
    await fetch(startEndpoint, {
        method: 'POST'
    })

}

const root = createRoot(document.getElementById("app"));

root.render(<button name="start" onClick={start_game}>Начать</button>);

