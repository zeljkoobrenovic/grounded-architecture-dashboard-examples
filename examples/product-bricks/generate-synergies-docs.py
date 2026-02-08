import json
import datetime

capabilities = json.load(open('data/capabilities.json'))
adoption = json.load(open('data/synergies.json'))
template = open('templates/synergies.html').read();
dateString = datetime.date.today().strftime('%Y-%m-%d')

htmlFile = 'docs/synergies.html'
print(htmlFile)
with open(htmlFile, 'w') as html_file:
    content = template\
        .replace('${date}', dateString)\
        .replace('${capabilities}', json.dumps(capabilities['data'][0]['data']))\
        .replace('${data}', json.dumps(adoption))
    html_file.write(content)

