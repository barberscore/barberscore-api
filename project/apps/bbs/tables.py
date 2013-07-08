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


class ContestTable(tables.Table):
    __unicode__ = tables.LinkColumn('contest', args=[A('slug')])

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class ContestantTable(tables.Table):
    __unicode__ = tables.LinkColumn('contestant', args=[A('slug')])

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class ScoreTable(tables.Table):
    __unicode__ = tables.LinkColumn('score', args=[A('slug')])

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}
