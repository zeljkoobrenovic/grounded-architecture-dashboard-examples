import json

active = json.load(open('data/active.json'))
archived = json.load(open('data/archived.json'))
template = open('templates/apps.html').read();

htmlFile = 'docs/index.html'
print(htmlFile)
with open(htmlFile, 'w') as html_file:
    html_file.write(template.replace('${active}', json.dumps(active))
                    .replace('${archived}', json.dumps(archived)))
