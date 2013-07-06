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
    contestant = tables.LinkColumn('contestant', args=[A('contestant.slug')])
    prelim = ScoreColumn()
    seed = tables.Column()
    # song_one = tables.Column()
    # score_one = ScoreColumn()
    # song_two = tables.Column()/
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


class ScoreTable(tables.Table):
    # slot = tables.Column()
    # stage_time = TimeColumn()
    place = tables.Column()
    # seed = tables.Column()

    contestant = tables.LinkColumn('contestant', args=[A('contestant.slug')])
    # prelim = ScoreColumn()
    name_one = tables.Column()
    # score_one = ScoreColumn()
    name_two = tables.Column()
    # score_two = ScoreColumn()
    avg_total_score = ScoreColumn()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}
