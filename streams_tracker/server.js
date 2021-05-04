const port = process.env.PORT || 8000;
var Server = require('./openwebtorrent-tracker').Server;

var server = new Server({
    udp: false, // enable udp server? [default=true]
    http: false, // enable http server? [default=true]
    ws: true, // enable websocket server? [default=true]
    stats: true, // enable web-based statistics? [default=true]
})

server.on('error', function (err) {
    console.log(err.message);
})

server.on('warning', function (err) {
    // client sent bad data. probably not a problem, just a buggy client.
    console.log(err.message);
})

server.on('listening', function () {
    // fired when all requested servers are listening
    console.log('listening on ws port: ' + server.ws.address().address + ":" + server.ws.address().port);
})

// start tracker server listening! Use 0 to listen on a random free port.
server.listen(port, "0.0.0.0");
