
# Third-Party
from algoliasearch_django import AlgoliaIndex


class ConventionIndex(AlgoliaIndex):
    fields = [
        'name',
    ]
    settings = {
        'searchableAttributes': [
            'name',
        ]
    }
