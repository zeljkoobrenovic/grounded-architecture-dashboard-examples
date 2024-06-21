import json

config = json.load(open('../../config.json'))
capabilities = json.load(open('../../data/details.json'))

def capability_by_name(name):
    for cap in capabilities['data'][0]['data']:
        if cap['capability'].lower().strip() == name.lower().strip():
            return cap;

    return None;

arch_states = json.load(open('../../data/metamorphosis.json'))

for capability in arch_states['data']:
    capability['info'] = capability_by_name(capability['source'])

with open('docs/capabilities.html', 'w') as html_file:
    template = open('templates/states.html').read()
    content = template.replace('${capabilities_info}', json.dumps(capabilities['data'][0]['data']))
    content = content.replace('${capabilities}', json.dumps(arch_states))
    html_file.write(content)

with open('docs/events.html', 'w') as html_file:
    template = open('templates/events.html').read()
    content = template.replace('${capabilities}', json.dumps(arch_states))
    html_file.write(content)

with open('docs/apis.html', 'w') as html_file:
    template = open('templates/apis.html').read()
    content = template.replace('${capabilities}', json.dumps(arch_states))
    html_file.write(content)

with open('docs/data-models.html', 'w') as html_file:
    template = open('templates/data-models.html').read()
    content = template.replace('${capabilities}', json.dumps(arch_states))
    html_file.write(content)

with open('docs/tech-debt.html', 'w') as html_file:
    template = open('templates/tech-debt.html').read()
    content = template.replace('${capabilities}', json.dumps(arch_states))
    html_file.write(content)

with open('docs/summary.html', 'w') as html_file:
    template = open('templates/summary.html').read()
    content = template.replace('${capabilities}', json.dumps(arch_states))
    html_file.write(content)

with open('docs/index.html', 'w') as html_file:
    template = open('templates/index.html').read()
    content = template.replace('${data_sheet}', config['sheets']['metamorphosis'])
    html_file.write(content)

