import sys, argparse, csv, re
import redis
from redisearch import Client

class CSVImporter: 
    def __init__(self, args):
        self.host = args.host
        self.port = args.port
        self.search = False
        self.index = args.index
        if self.index is not None:
            self.search = True
            self.search_client  = Client(self.index, self.host, self.port)
            self.info = self.search_client.info()['fields']
        self.file = open(args.file, 'r')
        self.delimiter = args.delimiter
        self.rows = args.rows
        self.ignore = args.ignore
        self.docid = args.docid
        self.client = redis.Redis(args.host, args.port)
        self.fields = [] 
        
    def addRow(self, row, num):
        values = dict()
        row_id = row[0]
        geo_id = 'zip-'
        geo_pos = ''
        lat = 0
        lon = 0
        idx = 0
        fieldnum = 0
        for val in row:
            idx += 1
            if self.fields[idx - 1] == 'regionidzip':
                geo_id += val
            if self.fields[idx - 1] == 'latitude':
                lat = float(val) / 1000000
            if self.fields[idx - 1] == 'longitude':
                lon = float(val) / 1000000

            if self.ignore is not None and idx in self.ignore or idx == self.docid:
                continue

            if self.search == True and self.info[fieldnum][2] == 'NUMERIC' and val == '':
                val = '0'
 
            values[self.fields[idx - 1]] = val
            fieldnum += 1       
        values['geopos'] = str(lon) + ',' + str(lat)
        geo_vals = [lon, lat, row_id]
            
        self.client.geoadd(geo_id, *geo_vals)
        if self.search == True:
            doc = 'doc-' + str(num)
            if self.docid > 0:
                doc = row[self.docid - 1]
            
            self.search_client.add_document(doc, replace=True, **values)
        else:
            self.client.hmset(row_id, values)

    def loafFile(self):
        reader = csv.reader(self.file, delimiter=self.delimiter)
        self.fields = next(reader)
        n = 0
        for row in reader:
            if self.rows > 0 and n == self.rows:
                break
            self.addRow(row, n)
            n += 1

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
        '-i, --index', dest='index', type=str,  help='Index name')
    parser.add_argument(
        '-f, --file', dest='file', type=str,  help='CSV file path', required=True)
    parser.add_argument(
        '-d, --delimiter', dest='delimiter', type=str, help='Delimiter',
        default=',')
    parser.add_argument(
        '-n, --rows', dest='rows', type=int, help='Number of rows to import',
        default=0)
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

