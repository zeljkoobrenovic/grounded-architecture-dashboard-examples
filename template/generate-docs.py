import json
import datetime

data = json.load(open('data/data.json'))
source_link = 'https://google.com'
dateString = datetime.date.today().strftime('%Y-%m-%d')

with open('docs/example.html', 'w') as html_file:
    template = open('templates/template.html').read();
    html_file.write(template
                    .replace('${date}', dateString)
                    .replace('${source_link}', source_link)
                    .replace('${data}', json.dumps(data)))

with open('docs/searchable.html', 'w') as html_file:
    template = open('templates/searchable.html').read();
    html_file.write(template
                    .replace('${date}', dateString)
                    .replace('${source_link}', source_link)
                    .replace('${data}', json.dumps(data)))

