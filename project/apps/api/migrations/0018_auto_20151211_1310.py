# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20151211_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='cutoff',
            field=models.FloatField(help_text=b"\n            If the qual type is 'score', enter the cutoff  as percentile.  If it is 'rank', enter as integer.", null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='rounds',
            field=models.IntegerField(blank=True, help_text=b'\n            The number of rounds that will be used in determining the contest.  Note that this may be fewer than the total number of rounds (rounds) in the parent session.', null=True, choices=[(3, 3), (2, 2), (1, 1)]),
        ),
    ]
