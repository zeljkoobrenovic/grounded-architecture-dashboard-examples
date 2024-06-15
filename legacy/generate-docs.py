import json
import datetime

data = json.load(open('data/legacy.json'))
dateString = datetime.date.today().strftime('%Y-%m-%d')

print('docs/index.html')
with open('docs/index.html', 'w') as html_file:
    template = open('templates/template.html').read();
    html_file.write(template.replace('${date}', dateString).replace('${data}', json.dumps(data['data'])))

