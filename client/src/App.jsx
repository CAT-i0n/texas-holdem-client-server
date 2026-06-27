import { useState } from 'react';
import { START_ENDPOINT, WEBSOCKET_URL } from "./Consts";
import { Game } from "./Game";



export function App() {
    const [appState, setAppState] = useState("EnterName");
    const [gameState, setGameState] = useState(false)
    const connect_to_ws = (playerName) => {
        const ws = new WebSocket(WEBSOCKET_URL + playerName)
        ws.onopen = async () => {
            await fetch(START_ENDPOINT, {
                method: 'POST'
            })
        };
        ws.onmessage = (event) => {

            const state = JSON.parse(event.data)
            setGameState(<div>
                <Game gameState={state} playerName={playerName} ws={ws} />
            </div>)
            setAppState("Game")
        };
        ws.onclose = () => {
            setAppState("EnterName")
        };
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
        ws.send_data = (move, bet = NaN) => {
            ws.send(JSON.stringify({ "move": move, "bet": bet }))
        }
        return ws
    }
    const start_game = async (playerName) => {
        setAppState("Loading")
        const ws = connect_to_ws(playerName)
    }


    const render = () => {
        switch (appState) {
            case "EnterName": {
                const continueGame = () => {
                    const name = document.getElementById('playerName').value.trim();
                    if (name) {
                        start_game(name)
                    }
                }
                return (<div className="menu">
                    <input className="menu-element" type="text" id="playerName" placeholder="Введите имя" />
                    <button className="menu-element" onClick={() => continueGame()}>Продолжить</button>
                </div>)
            }
            case "Loading": return (<div className="loader"></div>)
            case "Game": return (gameState)
        }
    }

    return (<div className="screen">
        {render()}
    </div>)
}
