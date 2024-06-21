import json

roadmap = open('roadmap.tsv').read().split('\n')
export = []

for line in roadmap:
    elements = line.split('\t')
    domain = elements[0].strip()
    capability = elements[1].strip()
    man_months = elements[2].strip()

    object = {
        'domain': domain,
        'capability': capability,
        'man_months': man_months,
        'months': []
    }

    export.append(object)

    if len(elements) > 3:
        i = 3

        for year in range(2024, 2027):
            start = 1

            for month in range(start, 13):
                month = {
                    'year': year,
                    'month': month,
                    'buildEffort': 0,
                    'maintenanceEffort': 0,
                }

                object['months'].append(month)

                if len(elements) > i:
                    month['buildEffort'] = int('0' + elements[i])
                    i += 1
                if len(elements) > i:
                    month['maintenanceEffort'] = int('0' + elements[i])
                    i += 1

with open('roadmap.json', 'w') as html_file:
    html_file.write(json.dumps(export))
