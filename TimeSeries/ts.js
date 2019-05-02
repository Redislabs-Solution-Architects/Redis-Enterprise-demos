var redis = require("redis")

var client = redis.createClient(6379, 'localhost');

var latest;
var latest_min;
var latest_max;

var delta = 20;
module.exports.getLatest = function(){
    var now = Math.floor(Date.now() / 1000);
    client.send_command('TS.RANGE', ['test-ts', now - delta, now] , function(err, reply) {
        latest = reply;
    });
    client.send_command('TS.RANGE', ['test-ts',  now - delta + 2, now, 'AGGREGATION', 'min', 3], function(err, reply) {
        latest_min = reply;
    });
    client.send_command('TS.RANGE', ['test-ts',  now - delta + 2, now, 'AGGREGATION', 'max', 3], function(err, reply) {
        latest_max = reply;
    });
   return { latest: latest, latest_min: latest_min, latest_max: latest_max };
};


