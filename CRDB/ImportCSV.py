
import sys, argparse, csv
from redisearch import Client

class CSVImporter: 
    def __init__(self, args):
        self.host = args.host
        self.port = args.port
        self.index = args.index
        self.file = open(args.file, 'r')
        self.delimiter = args.delimiter
        self.rows = args.rows
        self.hasHeader = args.header
        self.ignore = args.ignore
        self.docid = args.docid
        self.client  = Client(self.index, self.host, self.port)
        self.fields = self.client.info()['fields']
        
    def loafFile(self):
        reader = csv.reader(self.file, delimiter=self.delimiter)
        if self.hasHeader == True:
            next(reader)
        n = 0
        for row in reader:
            if self.rows > 0 and n == self.rows:
                break
            self.addRow(row)
            n += 1
        print('Finished loading ' + str(n) + ' rows.')
    
    def addRow(self, row):
        args = {}
        idx = 0
        fieldnum = 0
        for val in row:
            idx += 1
            if self.ignore is not None and idx in self.ignore or idx == self.docid:
                continue
            args[self.fields[fieldnum][0]] = val
            fieldnum += 1
        
        doc = 'doc' + str(idx)
        if self.docid > 0:
            doc = row[self.docid - 1]
        self.client.add_document(doc, replace=True, **args)
        
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
        '-i, --index', dest='index', type=str,  help='Index name', required=True)
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
    parser.add_argument(
        '-g, --ignore', dest='ignore', type=int, nargs='+', help='Ignore columns') 
    parser.add_argument(
        '-c, --doc-id', dest='docid', type=int, help='Document id column number',
        default=0)
    args= parser.parse_args()
    csv = CSVImporter(args)
    csv.loafFile()

if __name__ == '__main__':
    main()

