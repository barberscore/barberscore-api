# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0119_auto_20160212_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='year',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Qualified'), (20, b'Did Not Qualify'), (30, b'Disqualified'), (40, b'Dropped'), (50, b'Ranked'), (90, b'Final')]),
        ),
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set([('organization', 'long_name', 'kind', 'year')]),
        ),
    ]
