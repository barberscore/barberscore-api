from haystack import indexes

from .models import (
    Group,
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
