# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_auto_20150727_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spot',
            name='song',
            field=models.ForeignKey(related_name='arrangements', blank=True, to='api.Song', null=True),
        ),
    ]
