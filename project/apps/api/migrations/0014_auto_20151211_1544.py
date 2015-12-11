# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_remove_performance_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='goal',
            field=models.IntegerField(help_text=b'\n            The objective of the contest.', choices=[(1, b'Championship'), (2, b'Qualifier')]),
        ),
        migrations.AlterField(
            model_name='organization',
            name='level',
            field=models.IntegerField(blank=True, help_text=b'\n            The level of the contest.  Note that this may be different than the level of the parent session.', null=True, choices=[(1, b'International'), (2, b'District'), (3, b'Division')]),
        ),
    ]
