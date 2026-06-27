
export const CARD_SIZE = 50
export const VIEW_BOX_SIZE = {
    x: 1000,
    y: 650
}
export const CENTER_COORDS = {
    x: VIEW_BOX_SIZE.x / 2,
    y: VIEW_BOX_SIZE.y / 2
}

export const TABLE_PARAMS = {
    x: VIEW_BOX_SIZE.x * 0.42,
    y: VIEW_BOX_SIZE.y * 0.3
}


export const WINDOW_RATIO = VIEW_BOX_SIZE.x / VIEW_BOX_SIZE.y

export const START_ENDPOINT = `/start`
const wsProtocol = location.protocol === 'https:' ? 'wss' : 'ws';
export const WEBSOCKET_URL = `${wsProtocol}://${location.host}/connect/`;