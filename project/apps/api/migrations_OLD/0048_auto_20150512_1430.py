# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_auto_20150512_1042'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contest',
            options={'ordering': ('level', 'kind', '-year', 'district')},
        ),
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('-contest', 'place', '-score', '-prelim', 'group')},
        ),
        migrations.AlterModelOptions(
            name='convention',
            options={'ordering': ['district', '-year']},
        ),
        migrations.AddField(
            model_name='performance',
            name='mus1_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
    ]
