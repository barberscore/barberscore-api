
# Third-Party
from algoliasearch_django import AlgoliaIndex


class AwardIndex(AlgoliaIndex):
    fields = [
        'name',
        'get_kind_display',
        'get_level_display',
        'get_season_display',
        'get_age_display',
        'get_gender_display',
        'get_district_display',
        'get_division_display',
        'is_novice',
        'description',
    ]
    settings = {
        'searchableAttributes': [
            'name',
            'get_kind_display',
            'get_level_display',
            'get_season_display',
            'get_age_display',
            'get_gender_display',
            'get_district_display',
            'get_division_display',
        ],
        'attributesForFaceting': [
            'get_kind_display',
            'get_level_display',
            'get_season_display',
            'get_age_display',
            'get_gender_display',
            'get_district_display',
            'get_division_display',
        ]
    }
    should_index = 'is_searchable'


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


class ConventionIndex(AlgoliaIndex):
    fields = [
        'name',
        'get_district_display',
        'get_season_display',
        'year',
        'location',
        'venue_name',
        'image_url',
        'image_id',
    ]
    settings = {
        'searchableAttributes': [
            'get_district_display',
            'get_season_display',
            'year',
            'location',
            'venue_name',
        ],
        'attributesForFaceting': [
            'get_district_display',
            'get_season_display',
            'year',
        ]
    }
    should_index = 'is_searchable'


class GroupIndex(AlgoliaIndex):
    should_index = 'is_active'
    fields = [
        'name',
        'get_kind_display',
        'get_gender_display',
        'get_district_display',
        'get_division_display',
        'code',
        'bhs_id',
        'participants',
        'chapters',
        'is_senior',
        'is_youth',
        'description',
        'image_url',
        'image_id',
    ]
    settings = {
        'searchableAttributes': [
            'name',
            'code',
            'bhs_id',
            'participants',
            'chapters',
            'get_gender_display',
            'get_district_display',
            'get_division_display',
            'get_kind_display',
        ],
        'attributesForFaceting': [
            'get_kind_display',
            'get_gender_display',
            'get_district_display',
            'get_division_display',
            'is_senior',
            'is_youth',
        ]
    }
    should_index = 'is_searchable'


class PersonIndex(AlgoliaIndex):
    should_index = 'is_active'
    fields = [
        'name',
        'first_name',
        'last_name',
        'get_part_display',
        'get_gender_display',
        'get_district_display',
        'email',
        'home_phone',
        'work_phone',
        'cell_phone',
        'airports',
        'description',
        'bhs_id',
        'image_url',
        'image_id',
    ]
    settings = {
        'searchableAttributes': [
            'name',
            'first_name',
            'last_name',
            'get_part_display',
            'get_gender_display',
            'get_district_display',
            'email',
            'home_phone',
            'work_phone',
            'cell_phone',
            'airports',
            'description',
            'bhs_id',
        ],
        'attributesForFaceting': [
            'get_part_display',
            'get_gender_display',
            'get_district_display',
        ]
    }
    should_index = 'is_searchable'
