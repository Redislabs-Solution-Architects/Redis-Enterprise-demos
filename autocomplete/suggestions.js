
var redis = require("redis")

var endpoint = 'localhost'
var port = 6379

var ra = redis.createClient(port, endpoint);

module.exports.getSuggestions = function(input, fn) {
	ra.send_command('FT.SUGGET', ['comp', input], function(err, reply) {
		fn(reply)
	});
}

module.exports.addSuggestion = function(sugg) {
	ra.send_command('FT.SUGADD', ['comp', sugg, '1', 'INCR'])
}
