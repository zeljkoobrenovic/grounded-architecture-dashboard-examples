import json

data = json.load(open('data/apps.json'))
template = open('templates/apps.html').read();

htmlFile = 'docs/index.html'
print(htmlFile)
with open(htmlFile, 'w') as html_file:
    html_file.write(template.replace('${data}', json.dumps(data)))
