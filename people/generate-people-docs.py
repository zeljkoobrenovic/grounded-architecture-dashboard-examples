import json
import datetime

data = json.load(open('data/people.json'))
template = open('templates/group.html').read();

sources = []
date_string = datetime.date.today().strftime('%Y-%m-%d')
source_link = 'https://docs.google.com/spreadsheets/d/1rJnsBLEfYH3rtGXfahoOV8zXyhyAdMF1FNTaQXbFd7Y/edit?usp=sharing'

for source in data['data']:
    sourceName = source['source']
    htmlFile = 'docs/' + sourceName + '.html'
    sources.append({'name': sourceName, 'count': len(source['data'])})
    print(htmlFile)
    with open(htmlFile, 'w') as html_file:
        html_file.write(template.replace('${data}', json.dumps(source['data'])))

indexTemplate = open('templates/index.html').read();
with open('docs/index.html', 'w') as html_file:
    content = indexTemplate.replace('${data}', json.dumps(sources))
    content = content.replace('${date}', date_string)
    content = content.replace('${source_link}', source_link)

    html_file.write(content)
