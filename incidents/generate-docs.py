import json
import datetime

data = json.load(open('data/incidents.json'))
template = open('templates/incidents.html').read();

dateString = datetime.date.today().strftime('%Y-%m-%d')
source_link = 'https://docs.google.com/spreadsheets/d/1uXrO5P-ysGQWTgfMHasojYg7bRgfTZwNqpCKUIV_ekM/edit?usp=sharing'

def generate_html(source):
    htmlFile = 'docs/' + source['source'] + '.html'
    print(htmlFile)
    with open(htmlFile, 'w') as html_file:
        content = template.replace('${date}', dateString).replace('${data}', json.dumps(source['data']))
        html_file.write(content)


for source in data['data']:
    generate_html(source)

htmlFile = 'docs/index.html'
print(htmlFile)
with open(htmlFile, 'w') as html_file:
    content = template\
        .replace('${date}', dateString)\
        .replace('${source_link}', source_link)\
        .replace('${data}', json.dumps(data['data'][0]['data']))
    html_file.write(content)


