# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20150124_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='quartetmembership',
            name='contest',
            field=models.ForeignKey(default=None, blank=True, to='api.Contest', null=True),
            preserve_default=True,
        ),
    ]
