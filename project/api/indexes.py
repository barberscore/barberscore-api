from algoliasearch_django import AlgoliaIndex


class ChartIndex(AlgoliaIndex):
    fields = [
        'title',
        'arrangers'
    ]
    settings = {
        'searchableAttributes': [
            'title',
            'arrangers',
        ]
    }
