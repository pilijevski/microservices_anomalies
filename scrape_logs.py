import csv
import requests
import sys
from requests.auth import HTTPBasicAuth


def GetMetrixNames(url):
    new_url = '{0}/api/v1/label/__name__/values'.format(url)
    response = requests.get(new_url, auth=HTTPBasicAuth('admin', 'foobar'))
    names = response.json()['data']
    # Return metrix names
    return names


"""
Prometheus hourly data as csv.
"""

writer = csv.writer(open("metrics.csv", 'w'))
if len(sys.argv) != 2:
    print('Usage: {0} http://localhost:9090'.format(sys.argv[0]))
    sys.exit(1)
metrixNames = GetMetrixNames(sys.argv[1])
writeHeader = True
for metrixName in metrixNames:
    # now its hardcoded for hourly
    response = requests.get('{0}/api/v1/query'.format(sys.argv[1]), params={'query': metrixName + '[1s]'},
                            auth=HTTPBasicAuth('admin', 'foobar'))
    results = response.json()['data']['result']
    # Build a list of all labelnames used.
    # gets all keys and discard __name__
    labelnames = set()
    for result in results:
        labelnames.update(result['metric'].keys())
    # Canonicalize
    labelnames.discard('__name__')
    labelnames = sorted(labelnames)
    # Write the samples.
    if writeHeader:
        writer.writerow(['name', 'timestamp', 'value', 'labels'])
        writeHeader = False
    for result in results:
        row = [result['metric'].get('__name__', '')] + result['values'][0]
        l = []
        for label in labelnames:
            l.append(result['metric'].get(label, ''))
        writer.writerow(row + [l])
