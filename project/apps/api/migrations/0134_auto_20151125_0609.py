# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0133_auto_20151122_1634'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rank',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='rank',
            name='performance',
        ),
        migrations.RemoveField(
            model_name='rank',
            name='session',
        ),
        migrations.AddField(
            model_name='award',
            name='contest',
            field=models.ForeignKey(related_name='awards', blank=True, to='api.Contest', null=True),
        ),
        migrations.DeleteModel(
            name='Rank',
        ),
    ]
