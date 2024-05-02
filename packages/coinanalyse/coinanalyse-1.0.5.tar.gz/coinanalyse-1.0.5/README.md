#Explain about the arguments..
#'-s', '--seeds', help='target blockchain address(es)', dest='seeds'
#'-o', '--output', help='output file to save raw JSON data', dest='output'
#'-d', '--depth', help='depth of crawling', dest='depth', type=int, default=3
#'-t', '--top', help='number of addresses to crawl from results', dest='top', type=int, default=5
#'-l', '--limit', help='maximum number of addresses to fetch from one address', dest='limit', type=int, default=100

--- step1. About colors library ---
# Colors shouldn't be displayed in mac & lower version of windows, But also display in windows-10
# example 

from coinanalyse.colors import green, white, red, info, run, end
print ('''%s
  /\   _ _						 
 /--\  |  |  /_\   ||  \ /  ~  sss
/    \ |  | /   \  ||   /   &  e e   %sv1.0.4
%s''' % (green, white, end))

--- step2. Get response from bitcoin ---
#From BlockChain address '1AJbsFZ64EpEfS5UAjAfcUG8pH8Jn3rn1F'
#Getting Response -> Transaction history of a wallet with this address
import concurrent.futures

from coinanalyse.requester import requester

address = '1AJbsFZ64EpEfS5UAjAfcUG8pH8Jn3rn1F'

response = requester(address)
print(response)

--- step3 Prepare Addresses to crawl ---
#Prepare crawling transaction history of a wallet. -s address
#Prepare crawling multiple wallets. -s address1, address2	-> 1ETBbsHPvbydW7hGWXXKXZ3pxVh3VFoMaX
import argparse
from coinanalyse.utils import getNew
from coinanalyse.utils import ranker
from coinanalyse.colors import green, white, red, info, run, end

database = {}
parse = argparse.ArgumentParser()
parse.add_argument('-s', '--seeds', help='target blockchain address(es)', dest='seeds')
args = parse.parse_args()

seeds = args.seeds.split(',') if args.seeds else []
for seed in seeds:
    database[seed] = {}

database = ranker(database, 1)
toBeProcessed = getNew(database, set())
print(toBeProcessed)
print('%s %i addresses to crawl' % (info, len(toBeProcessed)))

--- step4. Crawling transaction history of wallet ---
#From Bitcoin address '1AJbsFZ64EpEfS5UAjAfcUG8pH8Jn3rn1F' 
#Crawling wallets...
database = {}
processed = set()

seeds = args.seeds.split(',') if args.seeds else []

for seed in seeds:
    database[seed] = {}

def crawl(addresses, processed, database, limit):
    threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    futures = (threadpool.submit(getTransactions, address, processed, database, limit) for address in addresses)
    for i, _ in enumerate(concurrent.futures.as_completed(futures)):
        print('%s Progress: %i/%i        ' % (info, i + 1, len(addresses)), end='\r')

try:
    for i in range(depth):
        print ('%s Crawling level %i' % (run, i + 1))
        database = ranker(database, top + 1)
        toBeProcessed = getNew(database, processed)
        print('%s %i addresses to crawl' % (info, len(toBeProcessed)))
        crawl(toBeProcessed, processed, database, limit)

--- Final Step. Analyse with Drawing ---
#Make the collected data to Json objects.

database = ranker(database, top)
jsoned = {'edges':[],'nodes':[]}

num = 0
doneNodes = []
doneEdges = []
for node in database:
    x, y = genLocation()
    size = len(database[node])
    if size > 20:
        size = 20
    if node not in doneNodes:
        doneNodes.append(node)
        jsoned['nodes'].append({'label': node, 'x': x, 'y': y, 'id':'id=' + node, 'size':size})
    for childNode in database[node]:
        uniqueSize = database[node][childNode]
        if uniqueSize > 20:
            uniqueSize = 20
        x, y = genLocation()
        if childNode not in doneNodes:
            doneNodes.append(childNode)
            jsoned['nodes'].append({'label': childNode, 'x': x, 'y': y, 'id':'id=' + childNode, 'size': uniqueSize})
        if (node + ':' + childNode or childNode + ':' + node) not in doneEdges:
            doneEdges.extend([(node + ':' + childNode), (childNode + ':' + node)])
            jsoned['edges'].append({'source':'id=' + childNode, 'target':'id=' + node, 'id':num, "size":uniqueSize/3 if uniqueSize > 3 else uniqueSize})
        num += 1

print('%s Total wallets:%i' % (info, len(jsoned['nodes'])))
print('%s Total connections:%i' % (info, len(jsoned['edges'])))

render = json.dumps(jsoned).replace(' ', '').replace('\'', '"')

#Support Formats :json
prepareGraph('%s.json' % seeds[0], render)

#If you want to view the collected data with a graph viewer of your choice, you can use -o option.
#example
#python3 test.py -s 1AJbsFZ64EpEfS5UAjAfcUG8pH8Jn3rn1F -o output.graphml

#Once the scan is complete, the graph will automatically open in your default browser. 
#If it doesn't open, open quark.html manually. 
#Don't worry if your graph looks messy like the one below or worse.
