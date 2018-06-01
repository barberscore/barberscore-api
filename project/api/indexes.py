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
    should_index = 'is_searchable'


class GroupIndex(AlgoliaIndex):
    should_index = 'is_active'
    fields = [
        'name',
        'get_kind_display',
        'get_gender_display',
        'code',
        'image',
        'bhs_id',
    ]
    settings = {
        'searchableAttributes': [
            'name',
            'code',
            'bhs_id',
            'get_kind_display',
        ],
        'attributesForFaceting': [
            'get_kind_display',
        ]
    }


class PersonIndex(AlgoliaIndex):
    fields = [
        'first_name',
        'middle_name',
        'last_name',
        'nick_name',
        'get_gender_display',
        'get_part_display',
        'email',
        'image',
        'bhs_id',
        'full_name',
        'common_name',
    ]
    settings = {
        'searchableAttributes': [
            'bhs_id,full_name',
            'get_gender_display',
            'get_part_display',
            'email',
        ]
    }
