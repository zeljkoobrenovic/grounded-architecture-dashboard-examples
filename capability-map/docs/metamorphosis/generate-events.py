import json
import re

arch_states = json.load(open('../../data/metamorphosis.json'))
sections = json.load(open('../../data/sections.json'))


def export_graph(state):
    fields = ['Event Topics (Receiving)', 'Event Topics (Sending)']
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
                        topic = re.sub('\\(.*', '', value).strip()

                        if not topicsMap.get(topic):
                            topicsMap[topic] = topic
                            topics.append(topic)

                        if 'sending' in row['section'].lower():
                            dependency = '"' + capability['source'] + '" -> "' + topic + '"'
                        else:
                            dependency = '"' + topic + '" -> "' + capability['source'] + '"'

                        dependencies += dependency + '\n'
                        print(dependency)

                        if not linksMap.get(dependency):
                            linksMap[dependency] = dependency
                            links.append({'source': '[' + capability['source'] + ']', 'target': topic, 'count': 1})

            if count > 0:
                dependencies += '"' + capability['source'] + '" [fillcolor=grey]\n'

    for topic in topics:
        dependencies += ' "' + topic + '" [image="../images/aws/Amazon-Simple-Notification-Service.png", imagepos="tc", height=0.9, labelloc="b", fontsize=10]\n'

    with open('docs/visuals/events/' + state + '.dot', 'w') as dot_file:
        template = open('templates/visuals/graphviz.dot').read()
        content = template.replace('${code}', dependencies)
        dot_file.write(content)

    with open('docs/visuals/events/' + state + '-3d.html', 'w') as dot_file:
        template = open('templates/visuals/force-graph-3d.html').read()
        content = template.replace('${data}', json.dumps(links))
        dot_file.write(content)


export_graph('current')
export_graph('planned')
export_graph('target')
