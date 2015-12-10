# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20151209_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='lvl',
            field=models.IntegerField(blank=True, help_text=b'\n            The level of the contest.  Note that this may be different than the level of the parent session.', null=True, choices=[(0, b'International'), (1, b'District'), (2, b'Division')]),
        ),
    ]
