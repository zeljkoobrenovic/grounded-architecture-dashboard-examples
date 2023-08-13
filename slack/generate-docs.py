import json
import datetime

data = json.load(open('data/slack.json'))
template = open('templates/slack.html').read();

dateString = datetime.date.today().strftime('%Y-%m-%d')


def generate_html(source):
    htmlFile = 'docs/' + source['source'] + '.html'
    print(htmlFile)
    with open(htmlFile, 'w') as html_file:
        content = template.replace('${date}', dateString).replace('${data}', json.dumps(source['data']))
        html_file.write(content)

def generate_filtered_html(source, filter_set):
    htmlFile = 'docs/' + source['source'] + '.html'
    print(htmlFile)
    with open(htmlFile, 'w') as html_file:
        content = template.replace('${date}', dateString).replace('${data}', json.dumps(source['data']))
        html_file.write(content)


for source in data['data']:
    generate_html(source)


