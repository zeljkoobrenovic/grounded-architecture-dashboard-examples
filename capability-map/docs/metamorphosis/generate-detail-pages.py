import json

capabilities = json.load(open('../../data/details.json'))

def capability_by_name(name):
    for cap in capabilities['data'][0]['data']:
        if cap['capability'].lower().strip() == name.lower().strip():
            return cap;

    return None;

arch_states = json.load(open('../../data/metamorphosis.json'))

for capability in arch_states['data']:
    capability_object = capability_by_name(capability['source'].strip())
    if capability_object != None:
        with open('docs/details/' + capability_object['id'] + '.html', 'w') as html_file:
            template = open('templates/details.html').read()
            content = template.replace('${capability}', json.dumps(capability_object))
            content = content.replace('${all_capabilities}', json.dumps(capabilities['data'][0]['data']))
            content = content.replace('${states}', json.dumps(capability['data']))
            html_file.write(content)
    else:
        print(capability['source'] + ' NOT FOUND')

