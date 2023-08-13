import json

data = json.load(open('data/summit.json'))
template = open('templates/summit.html').read();

htmlFile = 'docs/index.html'
print(htmlFile)
with open(htmlFile, 'w') as html_file:
    html_file.write(template.replace('${data}', json.dumps(data)))
