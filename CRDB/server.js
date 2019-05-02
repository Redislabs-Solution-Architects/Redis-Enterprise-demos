var cluster = require('cluster');
var express = require('express');
var app = express();
var http = require('http');
var server = http.createServer(app);
var io     = require('socket.io')(server);

const bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());

var dir = __dirname;

app.get('/', function(req, res) {
    res.sendFile(dir + '/crdb.html');
});

const args = require('yargs')
    .alias('e1', 'endpoint1')
    .demandOption('e1')
    .describe('e1', 'Endpoint 1 name or IP address')
    .string('e1')
    .alias('e2', 'endpoint2')
    .demandOption('e2')
    .describe('e2', 'Endpoint 2 name or IP address')
    .string('e2')
    .alias('p', 'port')
    .demandOption('p')
    .describe('p', 'Database port number')
    .number('p')
    .demandOption(['e1', 'e2', 'p']).argv;

var ra = require('./redisaccess.js')(args.endpoint1, args.endpoint2, args.port);
var cache = require('./cache.js');
var votes = require('./votes.js');
var game = require('./game.js');

var voteWorkers = [];
var gameWorkers = [];

function getCurrentCache() {
    io.emit('update_cache', cache.getCurrent());
};

function getCurrentVotes() {
    io.emit('update_votes', votes.getCurrent());
};

function getScores() {
    io.emit('update_scores', game.getCurrent());
};
function vote() {
   votes.vote(((cluster.worker.id + 1) % 2) + 1);
};


function doVote() {
   if (cluster.worker.id % 2 == 1) {
   	setInterval(vote, Math.floor(Math.random() * 1000) + 1);
  } else {
  	setInterval(vote, Math.floor(Math.random() * 2000) + 1000);
  }
};


function updateScore() {
   game.updateScore();
};

function doGame() {
   setInterval(updateScore, Math.floor(Math.random() * 2000) + 1);
};

io.on('connection', function(socket) {
   io.emit('update_cache', cache.getCurrent());
   io.emit('update_votes', votes.getCurrent());
});

app.post('/cache/:cluster', function(req, res) {
   cache.update(req.body.cache, req.params.cluster);
});

app.post('/start/vote', function(req, res) {
   var env = {"type": "vote"};
   voteWorkers.push(cluster.fork(env).id);
   voteWorkers.push(cluster.fork(env).id);

});

app.post('/stop/vote', function(req, res) {
   for (var id in cluster.workers) {
	if ( voteWorkers.indexOf(id) != 0 )
   	   cluster.workers[id].kill();
   }	
});

app.post('/start/game', function(req, res) {
   var env = {"type": "game"};
   gameWorkers.push(cluster.fork(env).id);
   gameWorkers.push(cluster.fork(env).id);

});

app.post('/stop/game', function(req, res) {
   for (var id in cluster.workers) {
        if ( gameWorkers.indexOf(id) != 0 )
           cluster.workers[id].kill();
   }
});

if (cluster.isWorker) {
    if ( process.env["type"] == "vote" ) {
    	doVote();
    } else if ( process.env["type"] == "game" ) {
        doGame();
   }
}
else {
    server.listen(8080);
    cache.reset();
    votes.reset();
    game.reset();
    setInterval(getCurrentCache, 1000);
    setInterval(getCurrentVotes, 1000);
    setInterval(getScores, 3000);
}

