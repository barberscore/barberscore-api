
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

class AwardIndex(AlgoliaIndex):
    fields = [
        'name',
        'get_kind_display',
        'get_gender_display',
        'get_representing_display',
    ]
    settings = {
        'searchableAttributes': [
            'name',
            'get_kind_display',
            'get_gender_display',
            'get_representing_display',
        ],
        'attributesForFaceting': [
            'get_kind_display',
            'get_gender_display',
        ]
    }


class GroupIndex(AlgoliaIndex):
    should_index = 'is_active'
    fields = [
        'name',
        'get_kind_display',
        'get_gender_display',
        'code',
        'get_representing_display',
        'get_division_display',
        'image_url',
        'image_id',
        'bhs_id',
        'owner_ids',
    ]
    settings = {
        'searchableAttributes': [
            'name',
            'code',
            'bhs_id',
            'get_representing_display',
            'get_division_display',
            'get_kind_display',
        ],
        'attributesForFaceting': [
            'get_kind_display',
        ]
    }


class PersonIndex(AlgoliaIndex):
    should_index = 'is_active'
    fields = [
        'first_name',
        'middle_name',
        'last_name',
        'nick_name',
        'get_gender_display',
        'get_part_display',
        'get_representing_display',
        'email',
        'image_url',
        'image_id',
        'bhs_id',
        'full_name',
        'common_name',
    ]
    settings = {
        'searchableAttributes': [
            'bhs_id,full_name',
            'get_gender_display',
            'get_part_display',
            'get_representing_display',
            'email',
        ]
    }

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


