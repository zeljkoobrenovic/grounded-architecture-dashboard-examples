import json
import datetime
import re

capabilities = json.load(open('../../data/capabilities.json'))
discussions = json.load(open('../../data/discussions.json'))
discussion_summaries_per_capability = json.load(open('../../data/summaries/summaries.json'))
synergies = json.load(open('../../data/synergies.json'))
planning = json.load(open('../../data/planning.json'))
roadmap = json.load(open('../../data/roadmap/roadmap.json'))
beebole_data = json.load(open('../../data/beebole.json'))
product_reviews = json.load(open('../../data/product_reviews.json'))
template = open('templates/landing_page.html').read();
templateCapex = open('templates/capex_form.html').read();
dateString = datetime.date.today().strftime('%Y-%m-%d')
targets = json.load(open('../../data/targets.json'))
legacy_links = json.load(open('../../data/wl-legacy-links.json'))

for capability in targets['data']:
    capability['data'] = [a for a in capability['data'] if a.get('brand_or_country') or a.get('capability')];


capabilities_map = {}
for capability in capabilities['data'][0]['data']:
    capabilities_map[capability['capability']] = capability

capabilities_summaries_map = {}
for summary in discussion_summaries_per_capability:
    cap_name = summary['capability']
    if capabilities_map.get(cap_name):
        capabilities_map[cap_name]['discussion_summary'] = summary['summary']

for discussion in discussions['data']:
    cap_name = discussion['source']
    if capabilities_map.get(cap_name):
        capabilities_map[cap_name]['discussions'] = discussion['data']

def target_by_name(name):
    for target in targets['data']:
        if target['source'].lower() == name.lower():
            return target['data']

    return []

def legacy_by_name(name):
    tech_debt = []
    for group in legacy_links['data']:
        for item in group['data']:
            if item.get('capability'):
                if item['capability'].lower().strip() == name.lower().strip():
                    item['group'] = group['source']
                    tech_debt.append(item)

    return tech_debt


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

    # product reviews
    capabilities_reviews = [
        {'id': '24', 'reviews': []},
        {'id': '23', 'reviews': []},
        {'id': '22', 'reviews': []},
        {'id': '21', 'reviews': []},
        {'id': '20', 'reviews': []},
        {'id': '19', 'reviews': []},
        {'id': '18', 'reviews': []},
        {'id': '17', 'reviews': []},
        {'id': '16', 'reviews': []},
        {'id': '15', 'reviews': []},
        {'id': '14', 'reviews': []},
        {'id': '13', 'reviews': []},
        {'id': '12', 'reviews': []},
        {'id': '11', 'reviews': []},
        {'id': '10', 'reviews': []},
        {'id': '9', 'reviews': []},
        {'id': '8', 'reviews': []},
        {'id': '7', 'reviews': []},
        {'id': '6', 'reviews': []},
        {'id': '5', 'reviews': []},
        {'id': '4', 'reviews': []},
        {'id': '3', 'reviews': []},
        {'id': '2', 'reviews': []},
        {'id': '1', 'reviews': []}
    ]
    capabilities_reviews_map = {}

    for review_group in capabilities_reviews:
        capabilities_reviews_map[review_group['id']] = review_group

    for review in product_reviews['data']:
        review_id = re.sub(r'\(.*', '', review['source']).strip()
        info = re.sub(r'.*?\(', '', review['source'])
        info = re.sub(r'\).*', '', info).strip()
        capabilities_reviews_map[review_id]['info'] = info
        for item in review['data']:
            if item.get('wl'):
                if item['wl'].lower() == name.lower():
                    capabilities_reviews_map[review_id]['reviews'].append(item)

    # planning and initiatives
    capabilities_planning = [
        {'cycle': '9', 'initiatives': []},
        {'cycle': '8', 'initiatives': []},
        {'cycle': '7', 'initiatives': []},
        {'cycle': '6', 'initiatives': []},
        {'cycle': '5', 'initiatives': []},
        {'cycle': '4', 'initiatives': []},
        {'cycle': '3', 'initiatives': []},
        {'cycle': '2', 'initiatives': []},
        {'cycle': '1', 'initiatives': []}
    ]
    capabilities_planning_map = {}

    for cycle in capabilities_planning:
        capabilities_planning_map[cycle['cycle']] = cycle

    for cycle in planning['data']:
        id = re.sub(r'Cycle ', '', cycle['source']).strip()
        if capabilities_planning_map.get(id):
            info = ''
            capabilities_planning_map[id]['info'] = info
            for item in cycle['data']:
                if item.get('wl'):
                    if item['wl'].lower() == name.lower():
                        capabilities_planning_map[id]['initiatives'].append(item)

    # roadmaps
    capability_roadmap = []

    for road in roadmap:
        if road['capability'].lower() == name.lower():
            capability_roadmap.append(road)

    # synergies and dependecies
    dependencies = []
    for dependency_group in synergies['data']:
        for dependency in dependency_group['data']:
            if dependency.get('capability') and dependency.get('dependency') and dependency['capability'].lower() == name.lower():
                dependency['image_id'] = capability_by_name(dependency['dependency'])['id']
                dependencies.append(dependency)

    reverse_dependencies = []
    for dependency_group in synergies['data']:
        for dependency in dependency_group['data']:
            if dependency.get('dependency') and dependency['dependency'].lower() == name.lower() and dependency.get('usage_commitment'):
                dependency['source'] = dependency_group['source']
                dependency['image_id'] = capability_by_name(dependency['capability'])['id']
                reverse_dependencies.append(dependency)

    # beebole

    capability_beebole = []
    capability_beebole_map = {}

    for year_data in beebole_data['data']:
        for beebole_item in year_data['data']:
            if beebole_item.get('capability') and beebole_item['capability'].lower() == name.lower() and beebole_item.get('days'):
                month_id = beebole_item['month'].split('-')
                map_id = beebole_item['capability'].lower() + '_' + beebole_item['month']
                days_in_month = float(beebole_item['days'] + '')
                if not capability_beebole_map.get(map_id):
                    beebole_cap_monthly_data = {
                        'year': month_id[0],
                        'month': month_id[1],
                        'fte': min(1, days_in_month / 22),
                        'people': []
                    }
                    beebole_cap_monthly_data['people'].append({'person': beebole_item['employee'], 'days': days_in_month})
                    capability_beebole.append(beebole_cap_monthly_data)
                    capability_beebole_map[map_id] = beebole_cap_monthly_data
                else:
                    capability_beebole_map[map_id]['fte'] += min(1, days_in_month / 22)
                    capability_beebole_map[map_id]['people'].append({'person': beebole_item['employee'], 'days': days_in_month})

    htmlFile = 'docs/' + str(capability['id']) + '.html'
    print(htmlFile)
    with open(htmlFile, 'w') as html_file:
        html_file.write(template
                        .replace('${date}', dateString)
                        .replace('${all_capabilities}', json.dumps(capabilities['data'][0]['data']))
                        .replace('${capability_name}', name.replace('&', '&amp;'))
                        .replace('${capability_data}', json.dumps(capability))
                        .replace('${capability_targets}', json.dumps(target_by_name(name)))
                        .replace('${beebole}', json.dumps(capability_beebole))
                        .replace('${planning}', json.dumps(capabilities_planning))
                        .replace('${roadmap}', json.dumps(capability_roadmap))
                        .replace('${dependencies}', json.dumps(dependencies))
                        .replace('${reverse_dependencies}', json.dumps(reverse_dependencies))
                        .replace('${tech_debt}', json.dumps(legacy_by_name(name)))
                        .replace('${product_reviews}', json.dumps(capabilities_reviews)))

    htmlFileCapex = 'docs/capex_form_' + str(capability['id']) + '.html'
    print(htmlFileCapex)
    with open(htmlFileCapex, 'w') as html_file:
        html_file.write(templateCapex
                        .replace('${date}', dateString)
                        .replace('${all_capabilities}', json.dumps(capabilities['data'][0]['data']))
                        .replace('${capability_name}', name.replace('&', '&amp;'))
                        .replace('${capability_data}', json.dumps(capability))
                        .replace('${capability_targets}', json.dumps(target_by_name(name)))
                        .replace('${beebole}', json.dumps(capability_beebole))
                        .replace('${planning}', json.dumps(capabilities_planning))
                        .replace('${roadmap}', json.dumps(capability_roadmap))
                        .replace('${dependencies}', json.dumps(dependencies))
                        .replace('${reverse_dependencies}', json.dumps(reverse_dependencies))
                        .replace('${product_reviews}', json.dumps(capabilities_reviews)))

