# Redis Graph Demo

This demo show redis graph

## Euro 2016
This demo contains data about football (socccer in the US) players, the teams they play for and the national teams they represent. 
Each player has a connection to a team and a national team.

### To load the data
```
cat create_euro2016.txt | redis-cli -h localhost -p 6379
```

### To run the queries
```
python GraphDemo.py -s localhost -p 6379 -g euro2016 -d euro2016_queries.txt
```

The GraphDemo python script runs all the queries in the euro2016_queries.txt file.
If you do not specify the -d parameter with the queries file, it runs in interactive mode and allows you to run any graph query 
on the given index.

## Air routes
This demo contains data about air routes between airports in the world.

### To load the data
```
python2 ImportCSV.py -s localhost -p 6379 -g air-routes -o nodes -r true -f air-routes-nodes.csv
python2 ImportCSV.py -s localhost -p 6379 -g air-routes -o edges -r true -f air-routes-edges.csv

```

### To run the queries
```
python GraphDemo.py -s localhost -p 6379 -g air-routes -d air-routes_queries.txt

```
The GraphDemo python script runs all the queries in the euro2016_queries.txt file.
If you do not specify the -d parameter with the queries file, it runs in interactive mode and allows you to run any graph query 
on the given index.
