# CRDB demo

This demo shows redis enterprise CRDB
It shows 3 different scenarios:
* Caching -  setting a string value.
* Voting - incrementing a numeric value.
* Game - Game leader board.

### Prerequisites
You should have a crdb database with 2 clusters created.

### To start the web app
'''
node server.js --e1 <cluster 1 fqdn> --e2 <cluster 2 fqdn> -p <database port number>
'''

You may need to install some packages using npm. For example, to install the redis node.js client, run:
```
npm install redis
```

### Use the web app

The web app constantly updates the data from both clusters for all keys.
You can set value for caching by entering the clue and clicking on the cluster button.
You can pause and resume the voting and the game to show how the values are eventual consistent.

You can disconnect the 2 cluster in order to show that each cluster continues to operate localy even if the is no sync bet ween the two.
you can do this by setting a firewall rule on the node that runs the proxy for cluster 1:
```
iptables -A INPUT -s <IP address of proxy node on cluster 2> -j DROP
```

You will see that the values are different for each cluster.

Then you can set the connection back by running:
```
iptables -F
```

After a few seconds the values should be the same on both clusters.
