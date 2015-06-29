from haystack import indexes

from .models import (
    Group,
    Contest,
    Singer,
    Song,
    Director,
)


class GroupIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Group
        fields = [
            'name',
            'slug',
            'description',
        ]


class ContestIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Contest
        fields = [
            'name',
            'slug',
            'description',
        ]


class SingerIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Singer
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


class DirectorIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Director
        fields = [
            'name',
            'slug',
            'description',
        ]
