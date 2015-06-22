# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0088_director_judge'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='baritone',
            field=models.ForeignKey(related_name='contestants_baritone', blank=True, to='api.Singer', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='bass',
            field=models.ForeignKey(related_name='contestants_bass', blank=True, to='api.Singer', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='director',
            field=models.ForeignKey(related_name='contestants', blank=True, to='api.Director', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='lead',
            field=models.ForeignKey(related_name='contestants_lead', blank=True, to='api.Singer', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='tenor',
            field=models.ForeignKey(related_name='contestants_tenor', blank=True, to='api.Singer', null=True),
        ),
    ]
