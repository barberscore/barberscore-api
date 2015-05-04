# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20150504_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='apperance',
            field=models.ForeignKey(blank=True, to='api.Appearance', null=True),
        ),
    ]
