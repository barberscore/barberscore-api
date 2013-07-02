import django_tables2 as tables
from django_tables2.utils import A


from .templatetags.bbstags import score, time_only


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


class PerformanceTable(tables.Table):
    # slot = tables.Column()
    stage_time = TimeColumn()
    contestant = tables.LinkColumn('rating', args=[A('slug')])
    prelim = ScoreColumn(accessor='contestant.prelim')
    seed = tables.Column(accessor='contestant.seed')
    song_one = tables.Column()
    # score_one = ScoreColumn()
    song_two = tables.Column()
    # score_two = ScoreColumn()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class ContestantTable(tables.Table):
    name = tables.LinkColumn('contestant', args=[A('slug')])
    # name = tables.Column()
    contestant_type = tables.Column()
    district = tables.Column()
    location = tables.Column()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class RatingTable(tables.Table):

    performance = tables.LinkColumn('rating', accessor='performance', args=[A('performance.slug')])
    contestant = tables.Column(accessor='performance.contestant')
    song_one = tables.Column()
    song_two = tables.Column()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}
