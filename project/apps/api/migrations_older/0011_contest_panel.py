# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_score_performance'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='panel',
            field=models.ForeignKey(related_name='contests', blank=True, to='api.Panel', null=True),
        ),
    ]
