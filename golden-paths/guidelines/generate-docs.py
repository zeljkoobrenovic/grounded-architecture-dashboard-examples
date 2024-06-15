import json
import datetime

data = json.load(open('data/paths.json'))
dateString = datetime.date.today().strftime('%Y-%m-%d')


def generate_paths():
    template = open('templates/paths.html').read();
    for group in data['data']:
        source = group['source'].lower()
        if source != 'owners':
            htmlFile = 'docs/' + source + '.html'
            print(htmlFile)
            with open(htmlFile, 'w') as html_file:
                html_file.write(template.replace('${date}', dateString).replace('${data}', json.dumps(group['data'])))

    with open('docs/overview.html', 'w') as overview_file:
        overview_template = open('templates/overview.html').read();
        overview_file.write(overview_template.replace('${date}', dateString).replace('${data}', json.dumps(data['data'])))

    with open('docs/summaries.html', 'w') as overview_file:
        overview_template = open('templates/summaries.html').read();
        overview_file.write(overview_template.replace('${date}', dateString).replace('${data}', json.dumps(data['data'])))

def generate_owners():
    owners_template = open('templates/owners.html').read();
    for group in data['data']:
        source = group['source'].lower()
        if source == 'owners':
            htmlFile = 'docs/' + source + '.html'
            print(htmlFile)
            with open(htmlFile, 'w') as html_file:
                html_file.write(owners_template.replace('${date}', dateString).replace('${data}', json.dumps(group['data'])))


generate_paths()
generate_owners()
