# Redis Time Series Demo
This demo shows redis time series data

### To load data
```
python LoadTS.py
```

This will load a constant stream of data to the redis time series database

### To start the web app
```
node server.js
```

You may need to install some packages using npm. For example, to install the redis node.js client, run:
```
npm install redis
```

## Use the web app
Open a browser and go to http://localhost:8080
You should see a graph showing the last 20 seconds of data and also the aggregated minimum and maximum over every 3 seconds.
