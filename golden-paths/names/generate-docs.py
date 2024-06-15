import json
import datetime

data = json.load(open('data/sites-brands.json'))
template = open('templates/brands-sites.html').read();
dateString = datetime.date.today().strftime('%Y-%m-%d')

htmlFile = 'docs/brands-sites.html'
print(htmlFile)
with open(htmlFile, 'w') as html_file:
    html_file.write(template.replace('${date}', dateString).replace('${data}', json.dumps(data)))

