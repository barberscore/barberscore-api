# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20150128_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(blank=True, to='api.Convention', null=True),
            preserve_default=True,
        ),
    ]
