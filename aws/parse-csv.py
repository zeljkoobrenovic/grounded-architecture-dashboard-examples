import csv
import json
import re


def ignore(name):
    # if name == 'Tax':
    #    return True
    if name.lower() == 'total cost':
        return True
    if name.lower() == 'total costs':
        return True
    if name.lower() == 'refund':
        return True
    if name.lower() == 'savings plans for  compute usage':
        return True
    if name.lower() == 'savings plans for compute usage':
        return True
    if name.lower().startswith('no tagkey'):
        return True
    if name.lower().startswith('ocb reinvent passes'):
        return True
    if name.lower().startswith('no database engine'):
        return True
    if name.lower().startswith('no instance type'):
        return True

    return False


def rename(name):
    if name.startswith('EC2'):
        return 'EC2'
    if name.startswith('db.'):
        return 'DB'
    if name.startswith('ml.'):
        return 'ML'
    if name.startswith('cache.'):
        return 'CACHE'

    info = {
        'm': 'general',
        't': 'general',
        'c': 'compute',
        'r': 'memory',
        'x': 'memory',
        'z': 'memory',
        'p': 'accelerate',
        'g': 'accelerate',
        'i': 'storage',
        'd': 'stroage',
    }
    letters = ['m', 't', 'r', 'c', 'g', 'i', 'ra', 'mac', 'dc', 'ds', 'p', 'x', 'z']

    for letter in letters:
        for i in range(1, 20):
            prefix = letter + str(i)
            if name.startswith(prefix):
                if (info.get(letter)):
                    return letter.upper() + ' ' + info[letter]
                else:
                    return letter.upper()

    if name.startswith('Kinesis'):
        return 'Kinesis'
    if name.startswith('AWS EMEA SARL'):
        return 'Amazon Web Services EMEA SARL'
    if name.startswith('Amazon Web Services, Inc.'):
        return 'Amazon Web Services EMEA SARL'
    return name


def process(awsgroup):
    with open('data/csv/' + awsgroup + '.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        firstRow = True

        columns = []
        months = []

        for row in csvreader:
            month = row[0]
            if len(month) == 10:
                month = month[0:7]
            if firstRow:
                firstColumn = True
                for item in row:
                    if not firstColumn:
                        service = item.replace('($)', '').strip()
                        service = re.sub('\:.*', '', service)
                        columns.append(service)
                    firstColumn = False

                firstRow = False
            else:
                if month.startswith('20'):
                    services = []
                    monthObject = {
                        'month': month,
                        'total': 0,
                        'services': services
                    }
                    months.append(monthObject)
                    i = 0
                    firstColumn = True
                    services_map = {}
                    for cost in row:
                        if not firstColumn:
                            column = columns[i]
                            i += 1
                            if not ignore(column):
                                value = 0;
                                if not cost == '':
                                    value = float(cost)
                                monthObject['total'] += value
                                print(column + ': ' + str(value))
                                column = rename(column)
                                if not services_map.get(column):
                                    services_map[column] = {
                                        'service': column,
                                        'usage': 0,
                                        'costs': value
                                    }
                                    services.append(services_map[column])
                                else:
                                    services_map[column]['costs'] += value
                        firstColumn = False

                    for item in monthObject['services']:
                        item['usage'] = item['costs'] / monthObject['total']

        jsonFile = 'data/json/' + awsgroup + '.json'
        print(jsonFile)
        active_columns = []
        for c in columns:
            if not ignore(c):
                c = rename(c)
                if not c in active_columns:
                    active_columns.append(c)
        with open(jsonFile, 'w') as html_file:
            html_file.write(json.dumps({'services': active_columns, 'perMonth': months}))


process('services')
process('regions')
process('api-operations')
