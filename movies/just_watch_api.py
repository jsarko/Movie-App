from justwatch import JustWatch

def get_providers(title):
    just_watch = JustWatch(country='US')

    results = just_watch.search_for_item(query=title)['items'][0]['offers']

    providers = {
        8: 'Netflix',
        9: 'Amazon',
        15: 'Hulu',
        27: 'HBO Now'
    }

    offered = []

    for item in results:
        p = providers.get(item['provider_id'])
        if p and p not in offered:
            offered.append(p)

    return offered