import json
import datetime

dateString = datetime.date.today().strftime('%Y-%m-%d')
data = json.load(open('data/backlog.json'))
architects = json.load(open('data/architects.json'))

# for Impact: Strategic Initiatives, if multiple ones only keep latest
scan_prefix = 'Impact: Strategic Initiatives'
strategic_initiatives_sources = [ d['source'] for d in data['data'] if d['source'].startswith(scan_prefix) ]
if len(strategic_initiatives_sources) > 1:
    data['data'] = [
        d for d in data['data']
        if not d['source'].startswith(scan_prefix) or d['source'] == max(strategic_initiatives_sources)
    ]

with open('docs/backlog.html', 'w') as html_file:
    template = open('templates/backlog.html').read();
    content = template\
        .replace('${date}', dateString)\
        .replace('${data}', json.dumps(data['data']))\
        .replace('${architects}', json.dumps(architects))
    html_file.write(content)

with open('docs/people.html', 'w') as html_file:
    template = open('templates/people.html').read();
    content = template\
        .replace('${date}', dateString)\
        .replace('${data}', json.dumps(data['data']))\
        .replace('${architects}', json.dumps(architects))
    html_file.write(content)

with open('docs/matrix.html', 'w') as html_file:
    template = open('templates/matrix.html').read();
    content = template\
        .replace('${date}', dateString)\
        .replace('${data}', json.dumps(data['data']))\
        .replace('${architects}', json.dumps(architects))
    html_file.write(content)
