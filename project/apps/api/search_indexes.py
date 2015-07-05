from haystack import indexes

from .models import (
    Group,
    # Contest,
    Song,
    Person,
)


class GroupIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Group
        fields = [
            'name',
            'slug',
            'description',
        ]


# class ContestIndex(indexes.ModelSearchIndex, indexes.Indexable):
#     class Meta:
#         model = Contest
#         fields = [
#             'name',
#             'slug',
#             'description',
#         ]


class PersonIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Person
        fields = [
            'name',
            'slug',
            'description',
        ]


class SongIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Song
        fields = [
            'name',
            'slug',
            'description',
        ]
