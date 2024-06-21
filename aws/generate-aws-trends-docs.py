import json
import datetime


def generate(dataFile, folder, mediaLinkPrefix):
    data = json.load(open('data/' + dataFile))
    template = open('templates/aws-trends.html').read()

    dateString = datetime.date.today().strftime('%Y-%m-%d')

    months = []

    for source in data['perMonth']:
        sourceName = source['month']
        months.append(sourceName)

    content = template

    content = content.replace('${all}', json.dumps(data['perMonth']))
    content = content.replace('${data}', json.dumps(data['perMonth'][-1]['services']))
    content = content.replace('${months}', json.dumps(months))
    content = content.replace('${date}', dateString)
    content = content.replace('${media-link-prefix}', mediaLinkPrefix)

    with open('docs/' + folder + '/trends.html', 'w') as html_file:
        html_file.write(content)

generate('json/services.json', 'services', 'https://zeljkoobrenovic.github.io/sokrates-media/')
generate('json/regions.json', 'regions', 'https://zeljkoobrenovic.github.io/sokrates-media/')
generate('json/accounts.json', 'accounts', 'https://zeljkoobrenovic.github.io/sokrates-media/')
generate('json/api-operations.json', 'api-operations', 'https://zeljkoobrenovic.github.io/sokrates-media/')
