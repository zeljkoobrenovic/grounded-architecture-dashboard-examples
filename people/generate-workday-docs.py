import json
import datetime

dateString = datetime.date.today().strftime('%Y-%m-%d')

def force_3d_graph():
    data = json.load(open('data/workday.json'))
    template = open('templates/force-graph-3d.html').read();

    with open('docs/workday-3d.html', 'w') as html_file:
        content = template.replace('${data}', json.dumps(data['data'][0]['data']))
        content = content.replace('${date}', dateString)

        html_file.write(content)


def html():
    data = json.load(open('data/workday.json'))
    template = open('templates/workday.html').read();

    with open('docs/workday.html', 'w') as html_file:
        content = template.replace('${data}', json.dumps(data['data'][0]['data']))
        content = content.replace('${date}', dateString)

        html_file.write(content)


force_3d_graph()
html()
