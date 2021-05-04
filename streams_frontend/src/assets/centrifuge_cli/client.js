import Centrifuge from 'centrifuge';
import { centrifuge_cli } from 'stores.js';
import { wss_host } from "host.js";


export async function init_ws() {
    disconnect_ws();
    let ws_token = localStorage.getItem('ws_token');
    const ws_client = new Centrifuge(`${wss_host}connection/websocket`);
    if (ws_token) {
        ws_client.setToken(ws_token);
    }
    ws_client.connect();
    centrifuge_cli.set(ws_client);
}

export function disconnect_ws() {
    centrifuge_cli.update(client => {
        if (client) {
            client.disconnect();
        }
        return client;
    });
}
