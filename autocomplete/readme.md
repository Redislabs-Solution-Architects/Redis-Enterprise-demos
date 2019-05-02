# Redis Search Auto Complete
This demo shows the auto complete capabilities of redis search

## To load data
```
python AddSuggestions.py  -s localhost -p 6379 -k comp -f countries.txt
```
This loads a list of all countries in the world to the database.

## To run the web app 
```
node server.js
```

You may need to install some packages using npm. For example, to install the redis node.js client, run:
```
npm install redis
```

## Use the web app
Open a browser and go to http://localhost:8080
In the text box, start typing a name of a country. You should see suggestions after typing 2 characters.
You can type any word and then enter, and it will be added to the database of suggestions.
