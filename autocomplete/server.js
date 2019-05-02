var express = require('express');
var app = express();
var http = require('http');
var server = http.createServer(app);

const bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());

var dir = __dirname;

app.use('/', express.static(dir + '/'))

var ac = require('./suggestions.js');

app.get('/', function(req, res) {
    res.sendFile(dir + '/auto-complete.html');
});


app.get('/complete', function(req, res) { 
    ac.getSuggestions(req.query.input, function(reply) {
    	res.send(reply);
    });
});

app.post('/update', function(req, res) {
   ac.addSuggestion(req.body.term);
   res.sendFile(dir + '/auto-complete.html');
});

server.listen(8080);
