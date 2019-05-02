
var ra = require('./redisaccess.js');

scores1 = [];
var scores2 = [];

var players = [ "John", "Jill", "Danny", "Rachel", "David", "Cathie" ]


module.exports.getCurrent = function() {
    ra.getRange('scores', 1, function(reply) {
        scores1 = reply;
    });

    ra.getRange('scores', 2, function(reply) {
        scores2 = reply;
    });

    return { scores1: scores1, scores2: scores2 };
};

module.exports.updateScore = function() {
   var name = players[Math.floor(Math.random() * players.length)];
   var score = Math.floor(Math.random() * 100) + 1;
   if ( Math.random() < 0.4 ) {
        ra.zincrby('scores', score, name, 1);
   } else {
        ra.zincrby('scores', score, name, 2);
   }

};

module.exports.reset = function() {
    ra.del('scores');
};

