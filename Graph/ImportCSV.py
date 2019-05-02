
import sys, argparse, csv, re
import redis
from redisgraph import Node, Graph

class CSVImporter: 
    def __init__(self, args):
        self.host = args.host
        self.port = args.port
        self.graph = args.graph
        self.file = open(args.file, 'r')
        self.object = args.object
        self.delimiter = args.delimiter
        self.rows = args.rows
        self.hasHeader = args.header
        self.redis = redis.Redis(args.host, args.port)
        self.client = Graph(self.graph, self.redis)
    
    def addNode(self, row):
        args = {}
        idx = 0
        if len(row) < 2 or row[1] != 'airport':
            return

        for val in row:
            idx += 1
            if idx == 1:
                args['id'] = int(val)
            elif idx == 4:
                args['code'] = val
            elif idx == 5:
                args['icao'] = val
            elif idx == 6:
                args['description'] = val
            elif idx == 11:
                args['country'] = val
            elif idx == 12:
                args['city'] = val
      
        print(args) 
        node = Node(label='airport', properties=args)
        self.client.add_node(node)
 
    def addEdge(self, row):
        if len(row) < 4 or row[3] != 'route':
            return

        idx = 0
        
        from_id = ''
        to_id = ''
        dist = ''
        for val in row:
            idx += 1
            if idx == 2:
                from_id = val
            elif idx == 3:
                to_id = val
            elif idx == 5:
                dist = val

        query = 'MATCH (from:airport { id: ' + from_id + ' }), (to:airport { id: ' + to_id + ' }) CREATE (from)-[:ROUTE {dist: ' + dist + ' }]->(to)'
        result = self.client.query(query)
         
    def loafFile(self):
        reader = csv.reader(self.file, delimiter=self.delimiter)
        if self.hasHeader == True:
            next(reader)
        n = 0
        for row in reader:
            if self.rows > 0 and n == self.rows:
                break
            if self.object == 'nodes':
                self.addNode(row)
            elif self.object == 'edges':
                self.addEdge(row)
            n += 1
        if self.object == 'nodes':
            self.client.commit()
        print('Finished loading ' + str(n) + ' rows.')
        
def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__)
    parser.add_argument(
        '-s, --host', dest='host', type=str, help='Server address',
        default='localhost')
    parser.add_argument(
        '-p, --port', dest='port', type=int, help='Server port',
        default=6379)
    parser.add_argument(
        '-g, --graph', dest='graph', type=str,  help='Graph name', required=True)
    parser.add_argument(
        '-o, --object', dest='object', type=str,  help='Objects to load, nodes or edges', required=True)
    parser.add_argument(
        '-f, --file', dest='file', type=str,  help='CSV file path', required=True)
    parser.add_argument(
        '-d, --delimiter', dest='delimiter', type=str, help='Delimiter',
        default=',')
    parser.add_argument(
        '-n, --rows', dest='rows', type=int, help='Number of rows to import',
        default=0)
    parser.add_argument(
        '-r, --header', dest='header', type=bool, help='Contains a header row',
        default=False)
    args= parser.parse_args()
    csv = CSVImporter(args)
    csv.loafFile()

if __name__ == '__main__':
    main()

