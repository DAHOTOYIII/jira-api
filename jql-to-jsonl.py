import requests
import csv
import urllib3
import tomllib
import io
from datetime import date
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open('config.toml', 'rb') as f:
    config = tomllib.load(f)
jql = config['jql']
username = config['username']
password = config['password']
step = int(config['batchsize'])  # default 100
baseurl = config['baseurl']
assert jql and username and password and step and baseurl, 'fill out all fields for config.toml'

start = 0

url = baseurl + '/sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?jqlQuery=' + jql

with open(f'results/jql-to-csv_{date.today()}.jsonl', 'w+') as f:
    # writer = csv.writer(f)

    while True:

        print(f'Getting {start}-{start+step}...')
        theurl = url + '&tempMax=' + str(step) + '&pager/start=' + str(start)
        resp = requests.get(theurl, auth=(username, password), verify=False)

        reader = csv.reader(io.StringIO(resp.text))
        # reader = csv.DictReader(io.StringIO(resp.text))

        header_dict = {}

        count = 1
        for r in reader:
            if count == 1:
                for i, field in enumerate(r):
                    if field not in header_dict.keys():
                        header_dict[field] = [i]
                    else:
                        header_dict[field] += [i]
            else:
                row = {}
                for field, indexes in header_dict.items():
                    row[field] = ' '.join([r[index] for index in indexes])

                f.write(json.dumps(row) + '\n')

            count += 1

        if count < step:  # might only work if the last page doesn't have exactly 100 records
            print(str(start + count) + ' issues exported')
            break

        start += step