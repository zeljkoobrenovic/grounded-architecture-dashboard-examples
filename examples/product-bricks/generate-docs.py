import json

# loading data
data = json.load(open('data/capabilities.json'))
targets = json.load(open('data/targets.json'))
discussions = json.load(open('data/discussions.json'))
discussion_summaries_per_month = json.load(open('data/summaries/summaries-per-month.json'))
legacy = json.load(open('data/legacy.json'))
tech_debt = json.load(open('data/wl-legacy-links.json'))

# adding targets to capabilities
for capability in targets['data']:
    capability['data'] = [a for a in capability['data'] if a.get('brand_or_country') or a.get('capability')];



def get_groups(capabilities_list):
    groups = {}
    groupsList = []
    sub_groups = {}

    def init_domain(domain):
        groups[domain] = []
        groupsList.append({'domain': domain, 'groups': groups[domain]})

    init_domain('Seeker / Buyer / Tenant')
    init_domain('Owner / Seller / Landlord')
    init_domain('Intermediary')
    init_domain('Data')
    init_domain('Platform Experience')

    for (item) in capabilities_list:
        domain = item['domain_ea'].strip()

        if domain not in groups:
            groups[domain] = []
            groupsList.append({'domain': domain, 'groups': groups[domain]})

        if item.get('group'):
            sub_group = item['group']
        else:
            sub_group = ''

        key = domain + '_' + sub_group

        if key not in sub_groups:
            sub_groups[key] = {'group': sub_group, 'items': []}
            groups[domain].append(sub_groups[key])

        item['inflight'] = not item.get('status') or not item['status'].lower().startswith('not')
        sub_groups[key]['items'].append(item)

    return groupsList


def process(all_list):
    all = get_groups(all_list)

    templateAllOverview = open('templates/all-overview.html').read()
    templateAllReport = open('templates/okr-report.html').read()
    templateAllOverviewTeams = open('templates/all-overview-teams.html').read()
    templateAllOverviewDiscussions = open('templates/all-overview-discussions.html').read()
    templateAllOverviewDiscussionsList = open('templates/all-overview-discussions-list.html').read()

    overviewAllContent = templateAllOverview.replace('${data}', json.dumps(all)).replace('${targets}', json.dumps(targets))
    overviewAllReport = templateAllReport.replace('${data}', json.dumps(all)).replace('${targets}', json.dumps(targets))
    overviewAllTeamsContent = templateAllOverviewTeams.replace('${data}', json.dumps(all))
    overviewAllDiscussionsContent = templateAllOverviewDiscussions.replace('${data}', json.dumps(all)).replace('${discussions}', json.dumps(discussions['data']))
    overviewAllDiscussionsContentList = templateAllOverviewDiscussionsList\
        .replace('${data}', json.dumps(all))\
        .replace('${summaries}', json.dumps(discussion_summaries_per_month))\
        .replace('${discussions}', json.dumps(discussions['data']))

    with open('docs/all-overview.html', 'w') as html_file:
        html_file.write(overviewAllContent)

    with open('docs/okr-report.html', 'w') as html_file:
        html_file.write(overviewAllReport)

    with open('docs/per-brand.html', 'w') as html_file:
        templatePerBrandReport = open('templates/per-brand.html').read()
        perBrandReport = templatePerBrandReport\
            .replace('${data}', json.dumps(all))\
            .replace('${legacy}', json.dumps(legacy))\
            .replace('${tech_debt}', json.dumps(tech_debt))\
            .replace('${targets}', json.dumps(targets))
        html_file.write(perBrandReport)

    with open('docs/all-overview-teams.html', 'w') as html_file:
        html_file.write(overviewAllTeamsContent)

    with open('docs/all-overview-discussions.html', 'w') as html_file:
        html_file.write(overviewAllDiscussionsContent)

    with open('docs/all-overview-discussions-list.html', 'w') as html_file:
        html_file.write(overviewAllDiscussionsContentList)


process(data['data'][0]['data'])
