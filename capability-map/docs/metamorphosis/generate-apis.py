import json
import re

arch_states = json.load(open('../../data/metamorphosis.json'))
sections = json.load(open('../../data/sections.json'))


def export_graph(state):
    fields = [
        # 'Event Topics (Receiving)',
        # 'Event Topics (Sending)',
        'API Dependencies (Internal)',
        'Web API Dependencies (Internal)',
        'Mobile API Dependencies (Internal)'
        'Internal APIs',
        'Public APIs',
        # 'BFF APIs'
    ]
    dependencies = '';
    topics = []
    topicsMap = {}
    links = []
    linksMap = {}
    for capability in arch_states['data']:
        for row in capability['data']:
            count = 0
            for field in fields:
                if row.get('section') and row['section'] == field and row.get(state):
                    count += 1
                    values = row[state].split('\n')

                    for value in values:
                        api = re.sub('\\(.*', '', value).strip()

                        if not topicsMap.get(api):
                            topicsMap[api] = api
                            topics.append(api)

                        if 'sending' in row['section'].lower():
                            dependency = '"' + capability['source'] + '" -> "' + api + '"'
                        else:
                            dependency = '"' + api + '" -> "' + capability['source'] + '"'

                        dependencies += dependency + '\n'

                        if not linksMap.get(dependency):
                            linksMap[dependency] = dependency
                            links.append({'source': '[' + capability['source'] + ']', 'target': api, 'count': 1})

            if count > 0:
                dependencies += '"' + capability['source'] + '" [fillcolor=grey]\n'

    for api in topics:
        dependencies += ' "' + api + '" [image="../../icons/backend.png", imagepos="tc", height=1.3, labelloc="b", fontsize=8]\n'

    with open('docs/visuals/apis/' + state + '.dot', 'w') as dot_file:
        template = open('templates/visuals/graphviz.dot').read()
        content = template.replace('${code}', dependencies)
        dot_file.write(content)

    with open('docs/visuals/apis/' + state + '-3d.html', 'w') as dot_file:
        template = open('templates/visuals/force-graph-3d.html').read()
        content = template.replace('${data}', json.dumps(links))
        dot_file.write(content)


export_graph('current')
export_graph('planned')
export_graph('target')
