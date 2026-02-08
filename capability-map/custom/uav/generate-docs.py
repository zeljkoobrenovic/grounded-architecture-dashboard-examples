import json

# loading data
capabilities = json.load(open('data/capabilities.json'))

with open('docs/index.html', 'w') as html_file:
    template = open('templates/index.html').read()
    content = template.replace('${capabilities}', json.dumps(capabilities))
    html_file.write(content)
