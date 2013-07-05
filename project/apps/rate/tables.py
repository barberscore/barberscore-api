import django_tables2 as tables
from django_tables2.utils import A

from apps.bbs.templatetags.bbstags import score, time_only


class ScoreColumn(tables.Column):
    def render(self, value):
        if value:
            return score(value)
        else:
            return None


class TimeColumn(tables.Column):
    def render(self, value):
        if value:
            return time_only(value)
        else:
            return None


class RatingTable(tables.Table):

    performance = tables.LinkColumn('rating', accessor='performance', args=[A('performance.slug')])
    contestant = tables.Column(accessor='performance.contestant')
    song_one = tables.Column()
    song_two = tables.Column()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class EnterRatingTable(tables.Table):
    # slot = tables.Column()
    stage_time = TimeColumn()
    contestant = tables.Column(accessor='contestant')
    performance = tables.LinkColumn('rating', accessor='slug', args=[A('slug')], verbose_name="Enter Rating")
    prelim = ScoreColumn()
    seed = tables.Column()
    # song_one = tables.Column()
    # score_one = ScoreColumn()
    # song_two = tables.Column()/
    # score_two = ScoreColumn()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}
