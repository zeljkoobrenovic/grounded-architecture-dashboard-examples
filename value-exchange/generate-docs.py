import json
import datetime

config = json.load(open('config.json'))
data = json.load(open('data/value-exchange.json'))
source_link = config['sheets']['data']
dateString = datetime.date.today().strftime('%Y-%m-%d')

with open('docs/index.html', 'w') as html_file:
    template = open('templates/value-exchange.html').read();
    html_file.write(template
                    .replace('${date}', dateString)
                    .replace('${source_link}', source_link)
                    .replace('${data}', json.dumps(data)))

