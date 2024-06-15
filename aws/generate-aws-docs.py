import json
import datetime

def generate(dataFile, folder, mediaLinkPrefix):
    data = json.load(open('data/' + dataFile))
    template = open('templates/aws.html').read()

    dateString = datetime.date.today().strftime('%Y-%m-%d')

    months = []

    for source in data['perMonth']:
        sourceName = source['month']
        months.append(sourceName)

    latestSource = {};

    for source in data['perMonth']:
        sourceName = source['month']
        print(sourceName)

        content = template.replace('${data}', json.dumps(source['services']))
        content = content.replace('${months}', json.dumps(months))
        content = content.replace('${totalCosts}', str(source['total']))
        content = content.replace('${focusMonth}', sourceName)
        content = content.replace('${date}', dateString)
        content = content.replace('${source}', sourceName.lower())
        content = content.replace('${sourceTitle}', sourceName)
        content = content.replace('${media-link-prefix}', mediaLinkPrefix)

        latestSource = source

        with open('docs/' + folder + '/' + sourceName.lower() + '.html', 'w') as html_file:
            html_file.write(content)

    sourceName = 'latest'
    print(sourceName)

    content = template.replace('${data}', json.dumps(data['perMonth'][-1]['services']))
    content = content.replace('${months}', json.dumps(months))
    content = content.replace('${totalCosts}', str(latestSource['total']))
    content = content.replace('${focusMonth}', data['perMonth'][-1]['month'])
    content = content.replace('${date}', dateString)
    content = content.replace('${source}', sourceName.lower())
    content = content.replace('${sourceTitle}', sourceName)
    content = content.replace('${media-link-prefix}', mediaLinkPrefix)

    with open('docs/' + folder + '/' + sourceName.lower() + '.html', 'w') as html_file:
        html_file.write(content)


generate('json/services.json', 'services', 'https://zeljkoobrenovic.github.io/sokrates-media/')
generate('json/regions.json', 'regions', 'https://zeljkoobrenovic.github.io/sokrates-media/')
generate('json/api-operations.json', 'api-operations', 'https://zeljkoobrenovic.github.io/sokrates-media/')
