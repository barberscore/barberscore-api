
# Third-Party
from algoliasearch_django import AlgoliaIndex


class AwardIndex(AlgoliaIndex):
    fields = [
        'name',
        'get_kind_display',
        'get_gender_display',
    ]
    settings = {
        'searchableAttributes': [
            'name',
            'get_kind_display',
            'get_gender_display',
        ],
        'attributesForFaceting': [
            'get_kind_display',
            'get_gender_display',
        ]
    }


class ConventionIndex(AlgoliaIndex):
    fields = [
        'name',
    ]
    settings = {
        'searchableAttributes': [
            'name',
        ]
    }
