import json
import datetime

config = json.load(open('config.json'))

indexTemplate = open('templates/index.html').read();
with open('docs/index.html', 'w') as html_file:
    work = json.load(open('data/work.json'))
    content = indexTemplate.replace('${work}', json.dumps(work))

    html_file.write(content)
