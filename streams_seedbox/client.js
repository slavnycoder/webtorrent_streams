const be_host = process.env.BACKEND_HOST;
const ws_host = process.env.WS_HOST;
const chunks_chan = process.env.CHUNKS_CHANNEL;

const http = require('http');
const axios = require('axios');
const WebTorrent = require('webtorrent-hybrid');
var Centrifuge = require("centrifuge");
const WebSocket = require('ws');

// init torrent client
var torrent_client = new WebTorrent(
  {
    torrentPort: 4444,
    tracker: {
      port: 6881
    }
  }
);
torrent_client.setMaxListeners(65535);
torrent_client.on('error', function (err) {
  console.log(err);
});

async function init_seedbox() {
  const settings_response = await axios.get(`https://${be_host}/api/settings/`);
  let ws_client = new Centrifuge(`wss://${ws_host}/connection/websocket`, {
    websocket: WebSocket
  });
  const token = settings_response.data.ws_token;
  ws_client.setToken(token);
  ws_client.subscribe(`chunks:${chunks_chan}`, new_message => {
    let new_torrent = torrent_client.add(new_message.data.torrent_url);
    new_torrent.on('error', function (err) {
      console.log(err);
    });
    setTimeout(() => {
      console.log(`${new_torrent.name} ${new_torrent.progress}`)
      new_torrent.destroy()
    }, 30 * 1000);
  });
  ws_client.on('connect', function (context) {
    console.log("Connected");
  });
  ws_client.connect();
}

init_seedbox();

const requestHandler = (request, response) => {
  console.log(request.url);
  response.end('Hello Node.js Server!');
}

const server = http.createServer(requestHandler);
server.listen(undefined, (err) => {
  if (err) {
    return console.log('err', err)
  }
})