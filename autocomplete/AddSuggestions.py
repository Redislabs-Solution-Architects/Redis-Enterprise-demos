import argparse
from redisearch import AutoCompleter, Suggestion

class SuggestionUpdater: 
    def __init__(self, args):
        self.host = args.host
        self.port = args.port
        self.key = args.key
        self.file = args.file
        self.rows = args.rows
        self.client =  AutoCompleter(self.key, self.host, self.port)
        
    def loadFile(self):
        suggs = []
        with open(self.file) as fp:  
            for cnt, line in enumerate(fp):
                line = line.strip()
                print("Line {}: {}".format(cnt, line))
                suggs.append(Suggestion(line, '1'))
                if cnt == self.rows - 1:
                    break 
            self.client.add_suggestions(*suggs)
            print('Finished loading ' + str(cnt) + ' rows.')
    

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
        '-k, --key', dest='key', type=str,  help='Key name', required=True)
    parser.add_argument(
        '-f, --file', dest='file', type=str,  help='Data file path', required=True)
    parser.add_argument(
        '-n, --rows', dest='rows', type=int, help='Number of rows to import',
        default=0)
    args = parser.parse_args()
    updater = SuggestionUpdater(args)
    updater.loadFile()

if __name__ == '__main__':
    main()

