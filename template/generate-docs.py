import json
import datetime

# loading config
config = json.load(open('config.json'))

data = json.load(open('data/data.json'))
dateString = datetime.date.today().strftime('%Y-%m-%d')

with open('docs/example.html', 'w') as html_file:
    template = open('templates/template.html').read()
    html_file.write(template
                    .replace('${date}', dateString)
                    .replace('${source_link}', config['sheets']['data'])
                    .replace('${data}', json.dumps(data)))

with open('docs/searchable.html', 'w') as html_file:
    template = open('templates/searchable.html').read()
    html_file.write(template
                    .replace('${date}', dateString)
                    .replace('${source_link}', config['sheets']['data'])
                    .replace('${data}', json.dumps(data)))

