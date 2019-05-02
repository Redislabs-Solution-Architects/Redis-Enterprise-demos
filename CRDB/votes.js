
var ra = require('./redisaccess.js');

var votes1 = '0';
var votes2 = '0';

module.exports.getCurrent = function() {
    ra.getValue('vote', 1, function(reply) {
        votes1 = reply;
    });
    ra.getValue('vote', 2, function(reply) {
        votes2 = reply;
    });
    
    return { votes1: votes1, votes2: votes2 };
};

module.exports.vote = function(dc) {
    ra.incr('vote', dc);
};

module.exports.reset = function() {
    ra.del('vote');
};

