# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0051_auto_20140701_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='appearance',
            field=models.IntegerField(help_text=b'\n            The appearance order, within a given round.', null=True, blank=True),
        ),
    ]
