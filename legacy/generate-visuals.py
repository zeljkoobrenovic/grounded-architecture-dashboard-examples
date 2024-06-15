import json
import re

legacy = json.load(open('data/legacy.json'))

def process_links(item, links, target_color, cell):
    dependencies = ''
    for link in links:
        fields = link.split(',')

        target = fields[0].strip()
        dependencies += '"' + target + '" [height=1, fillcolor=' + target_color + '];\n'
        dependencies += '"' + item[cell] + '" [fillcolor="#99000044"];\n'
        via = None
        info = None

        if len(fields) > 1: via = fields[1].strip()
        if len(fields) > 2: info = fields[2].strip()

        if via:
            dependencies += '"' + via + '" [fillcolor=lightgrey];\n'
            dependencies += '"' + item[cell] + '" -- "' + via + '" [penwidthj=3];\n'
            dependencies += '"' + via + '" -- "' + target + '";\n'
        else:
            dependencies += '"' + item[cell] + '" -- "' + target + '";\n'

    return dependencies


def get_clusters(cell):
    clusters = []
    cluster_map = {}
    index = 0
    for section in legacy['data']:
        for item in section['data']:
            if item.get('brand') and item.get(cell) and (item.get('wl_capability_links') or item.get('extra_links')):
                brand = item['brand']
                if not cluster_map.get(brand):
                    index += 1
                    cluster_map[brand] = {
                        'id': str(index),
                        'label': brand,
                        'nodes': []
                    }

                    clusters.append(cluster_map[brand])

                cluster_map[brand]['nodes'].append(item)

    return clusters


def export_graph(cell):
    dependencies = ''
    for cluster in get_clusters(cell):
        dependencies += 'subgraph cluster_' + cluster['id'] + ' {\n'
        dependencies += '    label="' + cluster['label'] + '"\n'
        dependencies += '    style="filled"\n'
        dependencies += '    color="#e4e4e4"\n'

        for node in cluster['nodes']:
            dependencies += '    "' + node[cell] + '";\n'

        dependencies += '}\n'

    for section in legacy['data']:
        for item in section['data']:
            if item.get(cell) and (item.get('wl_capability_links') or item.get('extra_links')):
                wl_links = []
                extra_links = []

                if item.get('wl_capability_links'):
                    wl_links = item['wl_capability_links'].split('\n')

                if cell == 'object' and item.get('extra_links'):
                    extra_links = item['extra_links'].split('\n')

                dependencies += process_links(item, extra_links, '"#99000044"', cell)
                dependencies += process_links(item, wl_links, 'lightblue', cell)

    print(dependencies)
    with open('docs/visuals/legacy-connections-' + cell + '.dot', 'w') as dot_file:
        template = open('templates/graphviz.dot').read()
        content = template.replace('${code}', dependencies)
        dot_file.write(content)


export_graph('object')
export_graph('brand')
