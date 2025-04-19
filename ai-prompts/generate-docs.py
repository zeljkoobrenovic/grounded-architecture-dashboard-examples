import json
import datetime

date_string = datetime.date.today().strftime('%Y-%m-%d')
prompts = json.load(open('data/index.json'))

for group in prompts:
    for prompt in group['prompts']:
        prompt_content = open('docs/' + prompt['file']).read()
        prompt['content'] = prompt_content

with open('docs/prompts.html', 'w') as html_file:
    template = open('templates/prompts.html').read()
    content = template.replace('${date}', date_string).replace('${prompts}', json.dumps(prompts))
    html_file.write(content)