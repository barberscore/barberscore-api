from haystack import indexes
from .models import Contestant


class ContestantIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        model = Contestant
