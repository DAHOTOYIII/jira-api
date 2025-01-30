import csv
import urllib3
import tomllib
import json
import io
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

desiredfields = [
    'Summary',
    'Status',
    'Priority',
    'Resolution',
    'Created',
    'Resolved',
]

with open('config.toml', 'rb') as f:
    config = tomllib.load(f)
jql = config['jql']
username = config['username']
password = config['password']
step = int(config['batchsize'])  # default 100
baseurl = config['baseurl']
assert jql and username and password and step and baseurl, 'fill out all fields for config.toml'

filename = input('What is the file you want to read (from ~/results)?')

url = baseurl + '/sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?jqlQuery=' + jql

output = []
with open('results/' + filename, 'r') as f:
    # reader = csv.DictReader(io.StringIO(f.read()))  # DictReader instead of reader, because desired fields have no duplicates
    rows = f.readlines()
    for row in rows:
        row_out = [None] * len(desiredfields)  # to set missing values to None
        for i, x in enumerate(desiredfields):
            row_out[i] = json.loads(row)[x]
        output.append(row_out)


with open('results/' + filename.split('.jsonl')[0] + '_ticket-status.csv', 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(desiredfields)
    for row in output:
        writer.writerow(row)


