# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0135_contestant_award'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entrant',
            options={'ordering': ('contest', 'group')},
        ),
        migrations.AlterField(
            model_name='performance',
            name='contestant',
            field=models.ForeignKey(related_name='performances', blank=True, to='api.Contestant', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='entrant',
            unique_together=set([('group', 'contest')]),
        ),
    ]
