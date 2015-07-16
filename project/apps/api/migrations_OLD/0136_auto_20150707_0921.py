# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0135_auto_20150707_0538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='singer',
            name='person',
        ),
        migrations.AddField(
            model_name='singer',
            name='persons',
            field=models.ForeignKey(related_name='singers', blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='singer',
            name='contestant',
            field=models.ForeignKey(related_name='singers', blank=True, to='api.Contestant', null=True),
        ),
    ]
