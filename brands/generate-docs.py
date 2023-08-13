import json
import datetime

data = json.load(open('data/brands.json'))
template = open('templates/brands.html').read();

date_string = datetime.date.today().strftime('%Y-%m-%d')
source_link = 'https://docs.google.com/spreadsheets/d/195iHjfUCGlHEREka2hvWxV9WWBeX9PfDp6OizYSWqiQ/edit?usp=sharing'

for source in data['data']:
    source_name = source['source']
    print(source_name)

    content = template.replace('${data}', json.dumps(source['data']))
    content = content.replace('${date}', date_string)
    content = content.replace('${source}', source_name.lower())
    content = content.replace('${source_title}', source_name)
    content = content.replace('${source_link}', source_link)

    with open('docs/' + source_name.lower() + '.html', 'w') as html_file:
        html_file.write(content.replace('class="hidden"', ''))

    with open('docs/' + source_name.lower() + '-embed.html', 'w') as html_file:
        html_file.write(content)