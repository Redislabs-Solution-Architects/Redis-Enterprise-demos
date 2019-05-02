
var redis = require("redis")

var dc1;
var dc2;

module.exports = function(endpoint1, endpoint2, port) {
   dc1 = redis.createClient(port, endpoint1);
   dc2 = redis.createClient(port, endpoint2);
};

function getDC(dc) {
	if ( dc == 1 )
		return dc1;
	else if (dc == 2 )
		return dc2;
};

module.exports.getValue = function(key, dc, fn) {
	getDC(dc).get(key, function(err, reply){
                fn(reply);
	});
};

module.exports.getRange = function(key, dc,  fn) {
	getDC(dc).zrevrange(key, 0, -1, 'withscores', function(err, reply) {
        fn(reply);
    });
};

module.exports.set = function(key, value, dc) {
        getDC(dc).set(key, value);
};

module.exports.incr = function(key, dc) {
	getDC(dc).incr(key);
};

module.exports.zincrby = function(key, score, name, dc) {
        getDC(dc).zincrby(key, score, name);
};

module.exports.del = function(key) {
        dc1.del(key);
};

