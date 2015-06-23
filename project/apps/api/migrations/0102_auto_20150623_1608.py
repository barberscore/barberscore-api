# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0101_remove_performance_men'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='chapter_name',
            field=models.CharField(help_text=b'\n            The name of the director(s) of the chorus.', max_length=200, null=True, blank=True),
        ),
    ]
