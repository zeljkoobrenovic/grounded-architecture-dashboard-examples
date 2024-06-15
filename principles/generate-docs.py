import json
import datetime

data = json.load(open('data/principles.json'))
template = open('templates/principles.html').read();
indexTemplate = open('templates/index.html').read();
dateString = datetime.date.today().strftime('%Y-%m-%d')

for group in data['data']:
    htmlFile = 'docs/' + group['source'] + '.html'
    print(htmlFile)
    with open(htmlFile, 'w') as html_file:
        html_file.write(template.replace('${date}', dateString).replace('${data}', json.dumps(group['data'])))

htmlIndexFile = 'docs/index.html'
with open(htmlIndexFile, 'w') as html_index_file:
    print(htmlIndexFile)
    html_index_file.write(indexTemplate.replace('${date}', dateString).replace('${data}', json.dumps(data['data'])))
