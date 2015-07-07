# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0136_auto_20150707_0921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='singer',
            name='persons',
        ),
        migrations.AddField(
            model_name='singer',
            name='person',
            field=models.ForeignKey(related_name='quartets', blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='directors',
            field=models.ManyToManyField(related_name='choruses', to='api.Person'),
        ),
    ]
