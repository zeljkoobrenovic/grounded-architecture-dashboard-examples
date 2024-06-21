import json

# loading config
config = json.load(open('config.json'))

# loading data
data = json.load(open('data/details.json'))
targets = json.load(open('data/targets.json'))
documents = json.load(open('data/documents.json'))

# adding targets to capabilities
for capability in targets['data']:
    capability['data'] = [a for a in capability['data'] if True];


def get_groups(capabilities_list):
    groups = {}
    groupsList = []
    sub_groups = {}

    def init_domain(domain):
        groups[domain] = []
        groupsList.append({'domain': domain, 'groups': groups[domain]})


    for domain in config['domains']:
        init_domain(domain['name'])

    for (item) in capabilities_list:
        domain = item['domain'].strip()

        if domain not in groups:
            groups[domain] = []
            groupsList.append({'domain': domain, 'groups': groups[domain]})

        if item.get('group'):
            sub_group = item['group']
        else:
            sub_group = ''

        key = domain + '_' + sub_group

        if key not in sub_groups:
            sub_groups[key] = {'group': sub_group, 'items': []}
            groups[domain].append(sub_groups[key])

        item['inflight'] = not item.get('status') or not item['status'].lower().startswith('not')
        sub_groups[key]['items'].append(item)

    return groupsList


def process(all_list):
    all = get_groups(all_list)

    with open('docs/index.html', 'w') as html_file:
        template = open('templates/index.html').read()
        content = template.replace('${documents_sheet}', config['sheets']['documents'])
        content = content.replace('${targets_sheet}', config['sheets']['targets'])
        content = content.replace('${dependencies_sheet}', config['sheets']['dependencies'])
        content = content.replace('${roadmap_sheet}', config['sheets']['roadmap'])
        content = content.replace('${details_sheet}', config['sheets']['details'])
        html_file.write(content)

    with open('docs/map.html', 'w') as html_file:
        template = open('templates/map.html').read()
        content = template.replace('${data}', json.dumps(all)).replace('${targets}', json.dumps(targets))
        content = content.replace('${config}', json.dumps(config))
        html_file.write(content)

    with open('docs/progress-report.html', 'w') as html_file:
        template = open('templates/progress-report.html').read()
        content = template.replace('${data}', json.dumps(all)).replace('${targets}', json.dumps(targets))
        html_file.write(content)

    with open('docs/map-discussions.html', 'w') as html_file:
        template = open('templates/map-discussions.html').read()
        content = template.replace('${data}', json.dumps(all)).replace('${discussions}', json.dumps(documents['data']))
        content = content.replace('${config}', json.dumps(config))
        html_file.write(content)

    with open('docs/map-discussions-list.html', 'w') as html_file:
        template = open('templates/map-discussions-list.html').read()
        content = template \
            .replace('${data}', json.dumps(all)) \
            .replace('${discussions}', json.dumps(documents['data']))
        html_file.write(content)


process(data['data'][0]['data'])
