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
    __unicode__ = tables.LinkColumn(
        'contest',
        args=[A('slug')],
        verbose_name="Contest")

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class ContestantTable(tables.Table):
    __unicode__ = tables.LinkColumn(
        'contestant',
        args=[A('slug')],
        verbose_name='Name')

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class QuartetTable(tables.Table):
    name = tables.LinkColumn(
        'contestant',
        args=[A('slug')],
        verbose_name='Name')
    leads = tables.Column(accessor='lead', verbose_name='Lead')  # rendering hack
    tenor = tables.Column()
    baritone = tables.Column()
    bass = tables.Column()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class ChorusTable(tables.Table):
    __unicode__ = tables.LinkColumn(
        'contestant',
        args=[A('slug')],
        verbose_name='Name')
    director = tables.Column()
    website = tables.Column()

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}


class ScoreTable(tables.Table):
    __unicode__ = tables.LinkColumn(
        'score',
        args=[A('slug')],
        verbose_name='Performance')

    class Meta:
        attrs = {"class": "table table-condensed table-bordered table-hover table-summary"}
