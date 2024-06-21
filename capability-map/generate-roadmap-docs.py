import json

config = json.load(open('config.json'))
data = json.load(open('data/roadmap/roadmap.json'))
capabilities = json.load(open('data/details.json'))

with open('docs/roadmap-report.html', 'w') as html_file:
    template = open('templates/roadmap-report.html').read()
    content = template.replace('${data}', json.dumps(data))
    content = content.replace('${capabilities}', json.dumps(capabilities['data'][0]['data']))
    html_file.write(content)

with open('docs/roadmap-per-capability.html', 'w') as html_file:
    template = open('templates/roadmap-per-capability.html').read()
    content = template.replace('${data}', json.dumps(data))
    html_file.write(content)

with open('docs/roadmap-sum.html', 'w') as html_file:
    template = open('templates/roadmap-sum.html').read()
    content = template.replace('${config}', json.dumps(config))
    content = content.replace('${data}', json.dumps(data))
    html_file.write(content)

with open('docs/roadmap-per-year.html', 'w') as html_file:
    template = open('templates/roadmap-per-year.html').read()
    content = template.replace('${data}', json.dumps(data))
    content = content.replace('${capabilities}', json.dumps(capabilities['data'][0]['data']))
    html_file.write(content)
