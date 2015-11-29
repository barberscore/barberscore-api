# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0135_auto_20151129_0512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='goal',
            field=models.IntegerField(blank=True, help_text=b'\n            The objective of the contest', null=True, choices=[(1, b'Championship'), (2, b'Prelims')]),
        ),
    ]
