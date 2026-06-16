import { createRoot } from "react-dom/client";
import { Game } from "./src/game";

const startEndpoint = "http://localhost:8000/start"


let ws = new WebSocket(`ws://localhost:8000/connect/player${String(Date.now()).slice(-4, -1)}`);

ws.onopen = () => {
    console.log('Connected to WebSocket server');
};
ws.onmessage = (event) => {
    const gameState = JSON.parse(event.data)
    root.render(
        <Game gameState={gameState} />
    )
    if (gameState?.options) {
        let x = 1
    }
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

