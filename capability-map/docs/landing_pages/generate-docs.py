import json
import datetime

# loading config
config = json.load(open('../../config.json'))

capabilities = json.load(open('../../data/details.json'))
documents = json.load(open('../../data/documents.json'))
dependency_data = json.load(open('../../data/dependencies.json'))
roadmap = json.load(open('../../data/roadmap/roadmap.json'))
targets = json.load(open('../../data/targets.json'))

template = open('templates/landing_page.html').read();

dateString = datetime.date.today().strftime('%Y-%m-%d')

for capability in targets['data']:
    capability['data'] = [a for a in capability['data'] if a.get('target')];

capabilities_map = {}
for capability in capabilities['data'][0]['data']:
    capabilities_map[capability['capability']] = capability

for discussion in documents['data']:
    cap_name = discussion['source']
    if capabilities_map.get(cap_name):
        capabilities_map[cap_name]['discussions'] = discussion['data']

def target_by_name(name):
    for target in targets['data']:
        if target['source'].lower() == name.lower():
            return target['data']

    return []


capabilities_name_index = {}

for capability in capabilities['data'][0]['data']:
    name = capability['capability']
    capabilities_name_index[name.lower().strip()] = capability


def capability_by_name(name):
    if capabilities_name_index.get(name.lower().strip()):
        return capabilities_name_index[name.lower().strip()]
    return {'id': 0}


for capability in capabilities['data'][0]['data']:
    name = capability['capability']

    # roadmaps
    capability_roadmap = []

    for road in roadmap:
        if road['capability'].lower() == name.lower():
            capability_roadmap.append(road)

    # synergies and dependencies
    dependencies = []
    for dependency_group in dependency_data['data']:
        for dependency in dependency_group['data']:
            if dependency.get('capability') and dependency.get('dependency') and dependency['capability'].lower() == name.lower():
                dependency['image_id'] = capability_by_name(dependency['dependency'])['id']
                dependencies.append(dependency)

    reverse_dependencies = []
    for dependency_group in dependency_data['data']:
        for dependency in dependency_group['data']:
            if dependency.get('dependency') and dependency['dependency'].lower() == name.lower() and dependency.get('usage_commitment'):
                dependency['source'] = dependency_group['source']
                dependency['image_id'] = capability_by_name(dependency['capability'])['id']
                reverse_dependencies.append(dependency)

    htmlFile = 'docs/' + str(capability['id']) + '.html'
    print(htmlFile)
    with open(htmlFile, 'w') as html_file:
        html_file.write(template
                        .replace('${date}', dateString)
                        .replace('${config}', json.dumps(config))
                        .replace('${all_capabilities}', json.dumps(capabilities['data'][0]['data']))
                        .replace('${capability_name}', name.replace('&', '&amp;'))
                        .replace('${capability_data}', json.dumps(capability))
                        .replace('${capability_targets}', json.dumps(target_by_name(name)))
                        .replace('${roadmap}', json.dumps(capability_roadmap))
                        .replace('${dependencies}', json.dumps(dependencies))
                        .replace('${reverse_dependencies}', json.dumps(reverse_dependencies)))
