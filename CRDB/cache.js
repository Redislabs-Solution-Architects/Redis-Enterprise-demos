
var ra = require('./redisaccess.js');

var cache1 = '';
var cache2 = '';

module.exports.getCurrent = function(){
    ra.getValue('cache', 1, function(reply) {
        cache1 = reply;
    });
    ra.getValue('cache', 2, function(reply) {
        cache2 = reply;
    });
    
    return { cache1: cache1, cache2: cache2 };
};

module.exports.update = function(val, dc) {
    ra.set('cache', val, dc);
};

module.exports.reset = function() {
    ra.del('cache');
};

