import django_tables2 as tables
from django_tables2.utils import A


class RatingTable(tables.Table):

    performance = tables.LinkColumn('rating', accessor='performance', args=[A('performance.slug')])
    contestant = tables.Column(accessor='performance.contestant')
    song_one = tables.Column()
    song_two = tables.Column()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}
