import redis, csv, argparse, datetime
from tabulate import tabulate

units = ['mi', 'm', 'km', 'ft']
headers = ['Distance', 'Year Built', 'Lot Size', 'Bedrooms', 'Bathrooms', 'Value', 'tax Amount']
fields = ['yearbuilt', 'lotsizesquarefeet', 'bedroomcnt', 'bathroomcnt',  'taxvaluedollarcnt', 'taxamount']

class GeoDemo:
    def __init__(self, args):
        self.redis = redis.Redis(args.host, args.port)

    def printResults(self, res):
        table = []
        for r in res:
            vals = self.redis.hmget(r[0], *fields)
            vals.insert(0, r[1])
            table.append(vals)
        print(tabulate(table, headers, tablefmt='grid'))           
            
   
    def interactive(self):
        zipcode = raw_input('Enter zip code:')
        while zipcode.upper() != 'QUIT' and zipcode.upper() != 'EXIT':
            input_dist = raw_input('Enter distance and unit [mi|m|km|ft]:')
            dist = input_dist.split()
            d = float(dist[0])
            u = dist[1]
            if u not in units:
                print('Invalid unit.')
                continue
            member = raw_input('Enter member:')
            res = self.redis.georadiusbymember('zip-' + zipcode, member, d, u, withdist=True,sort='ASC', count=10)
            self.printResults(res[1:])            
            zipcode = raw_input('Enter zip code:')

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
    args= parser.parse_args()

    geoDemo = GeoDemo(args)
    geoDemo.interactive()

if __name__ == '__main__':
    main()


