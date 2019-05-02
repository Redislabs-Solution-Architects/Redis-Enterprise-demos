var express = require('express');
var app = express();
var http = require('http');
var server = http.createServer(app);
var io     = require('socket.io')(server);

var dir = __dirname;

app.get('/', function(req, res) {
    res.sendFile(dir + '/index.html');
});

var ts = require('./ts.js');

function getCurrent() {
    io.emit('update_ts', ts.getLatest());
};

server.listen(8080);
setInterval(getCurrent, 1000);
