from haystack import indexes
from .models import Singer, Contestant


# class SingerIndex(indexes.ModelSearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     # # name = indexes.CharField(model_attr='name')

#     # def get_model(self):
#     #     return Singer

#     # def index_queryset(self, using=None):
#     #     """Used when the entire index for model is updated."""
#     #     return self.get_model().objects.all()

#     class Meta:
#         model = Singer


class ContestantIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        model = Contestant
