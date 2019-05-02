import redis, csv, argparse, datetime
from redisgraph import Graph
import readline

class GraphDemo: 
    def __init__(self, args):
        self.graph = args.graph
        self.redis = redis.Redis(args.host, args.port)
        self.client = Graph(self.graph, self.redis)

    def readQuery(self):
        query = raw_input('Enter query:')
        return query.strip()

    def removeDuplicates(self, res):
        row = 1
        while row < len(res):
           rs = sorted(res[row])
           idx = row + 1
           while idx < len(res):
               if rs == sorted(res[idx]):
                   res.pop(idx)
               idx += 1
           row += 1
        return res

    def executeQuery(self, query):
        res = None
        try:
            st = datetime.datetime.now()
            res = self.client.query(query)
            duration=(datetime.datetime.now() - st).total_seconds() * 1000
        except redis.exceptions.ResponseError, e:
            print('Error: ' + str(e))
            return
        res.result_set = self.removeDuplicates(res.result_set)
        res.pretty_print() 

    def runDemo(self, queriesFile):
        f = open(queriesFile, 'r')
        for line in f.readlines():
            line=line.strip()
            print(line)
            if line.startswith('#'):
                 continue
            raw_input("Press any key to execute the query...")
            print('\n')
            self.executeQuery(line)
            print('\n')
            raw_input("Press any key to go to the next query...")
            print('\n')

    def interactive(self):
        query = self.readQuery()
        while query.upper() != 'QUIT' and query.upper() != 'EXIT':
            if query != '':
                self.executeQuery(query)
            query = self.readQuery()

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
        '-d, --demo', dest='demo', type=str, help='Read queries from the specified file. Otherwise, runs in interactive mode')
    args= parser.parse_args()
   
    graphDemo = GraphDemo(args)
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set editing-mode vi')
    readline.set_completer_delims(' \t\n')

    if args.demo is not None:
        graphDemo.runDemo(args.demo)
    else:
        graphDemo.interactive()

if __name__ == '__main__':
    main()

