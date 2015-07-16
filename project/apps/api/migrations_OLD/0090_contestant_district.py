# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0089_auto_20150622_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='district',
            field=models.ForeignKey(related_name='contestants', blank=True, to='api.District', null=True),
        ),
    ]
