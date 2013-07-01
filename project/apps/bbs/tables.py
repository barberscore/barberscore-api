import django_tables2 as tables
from django_tables2.utils import A


from .templatetags.bbstags import score


class ScoreColumn(tables.Column):
    def render(self, value):
        if value:
            return score(value)
        else:
            return None


class PerformanceTable(tables.Table):
    slot = tables.Column()
    contestant = tables.LinkColumn('performance', args=[A('slug')])
    prelim = tables.Column(accessor='contestant.prelim')
    seed = tables.Column(accessor='contestant.seed')
    song_one = tables.Column()
    score_one = ScoreColumn()
    song_two = tables.Column()
    score_two = ScoreColumn()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class ContestTable(tables.Table):
    # name = tables.LinkColumn('contest_round', args=[A('slug'), A('contest_round')])
    name = tables.Column()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class ContestantTable(tables.Table):
    # name = tables.LinkColumn('contestant', args=[A('slug')])
    name = tables.Column()
    contestant_type = tables.Column()
    district = tables.Column()
    location = tables.Column()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class RatingTable(tables.Table):

    performance = tables.LinkColumn('rating', args=[A('performance.slug')])
    song_one = ScoreColumn()
    song_two = ScoreColumn()


    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}

