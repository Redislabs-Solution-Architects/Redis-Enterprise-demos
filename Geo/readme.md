# Geospatial Data Demo
This demo show redis geospatial data using the core redis geospatial indexes and also using redis search.
It contains data about properties listed in zillow. Each property contains the longitude and latitude so it can be used to do a geospatial data search.

## Core redis geospatial indexes

### To load the data
```
python ImportCSV.py -s localhost -p 6379 -c 1 -g 2 3 7 8 10 11 13 14 15 16 17 18 24 25 26 30 31 32 33 34 35 42 43 44 46 47 56 57 -f properties.csv
```

### Example of data querying
```
python2 GeoDemo.py -s localhost -p 6379
Enter zip code:96026
Enter distance and unit [mi|m|km|ft]:1 mi
Enter member:11459347
````

## Geospatial data with redis search

### To load the data
```
redis-cli -h localhost -p 6379
127.0.0.1:6379>FT.CREATE zillow schema basementsqft numeric sortable bathroomcnt numeric sortable bedroomcnt numeric sortable calculatedbathnbr numeric sortable calculatedfinishedsquarefeet numeric sortable fireplacecnt numeric sortable fullbathcnt numeric sortable garagecarcnt numeric sortable garagetotalsqft numeric sortable hashottuborspa text sortable lotsizesquarefeet numeric sortable poolcnt numeric sortable poolsizesum numeric sortable rawcensustractandblock text nostem sortable regionidcity text nostem sortable regionidcounty text nostem sortable regionidneighborhood text nostem sortable regionidzip text nostem sortable roomcnt numeric sortable unitcnt numeric sortable yearbuilt numeric sortable numberofstories numeric sortable fireplaceflag text sortable structuretaxvaluedollarcnt numeric sortable taxvaluedollarcnt numeric sortable assessmentyear numeric sortable landtaxvaluedollarcnt numeric sortable taxamount numeric sortable censustractandblock text nostem sortable geopos geo
127.0.0.1:6379>quit
python ImportCSV.py -s localhost -p 6379 -c 1 -g 2 3 7 8 10 11 13 14 15 16 17 18 24 25 26 30 31 32 33 34 35 42 43 44 46 47 56 57 -f properties.csv -i zillow
```

### To run the queries
```
python2 ../Search/SearchDemo.py -s localhost -p 6379 -i zillow -d queries.txt
```

The SearchDemo python script runs all the quries in the queries.txt file.
If you do not specify the -d parameter with the queries file, it run in interactive mode and allows you to run any search query on the given index.
