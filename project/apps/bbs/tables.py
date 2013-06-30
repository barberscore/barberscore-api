import django_tables2 as tables
from django_tables2.utils import A

from .models import (Score)

from .templatetags.bbstags import score


class ScoreColumn(tables.Column):
    def render(self, value):
        if value:
            return score(value)
        else:
            return None


class BootstrapTable(tables.Table):

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class PerformanceTable(tables.Table):
    slot = tables.Column()
    __unicode__ = tables.LinkColumn('performance', args=[A('pk')])
    # contestant_type = tables.Column(accessor='contestant.contestant_type')
    # contest_round = tables.Column()
    song_one = tables.Column()
    score_one = ScoreColumn()
    song_two = tables.Column()
    score_two = ScoreColumn()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class ConventionTable(tables.Table):
    __unicode__ = tables.LinkColumn('convention', args=[A('slug')])

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class ContestantTable(tables.Table):
    name = tables.LinkColumn('contestant', args=[A('slug')])
    contestant_type = tables.Column()
    district = tables.Column()
    location = tables.Column()
    prelim = ScoreColumn()
    seed = tables.Column()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class ScoreTable(tables.Table):

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}
        model = Score
