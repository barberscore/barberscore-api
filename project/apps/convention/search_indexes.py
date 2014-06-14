from haystack import indexes
from .models import Contestant


class ContstantIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Contestant
