from haystack import indexes
from .models import Contestant


class ContestantIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Indexes the Contestant models.
    """

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Contestant
