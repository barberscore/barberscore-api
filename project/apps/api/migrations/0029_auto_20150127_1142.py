# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20150127_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='chorus',
            name='prelim',
            field=models.FloatField(help_text=b'\n            The incoming prelim score.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chorus',
            name='rank',
            field=models.IntegerField(help_text=b'\n            The incoming rank (based on prelim).', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartet',
            name='prelim',
            field=models.FloatField(help_text=b'\n            The incoming prelim score.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartet',
            name='rank',
            field=models.IntegerField(help_text=b'\n            The incoming rank (based on prelim).', null=True, blank=True),
            preserve_default=True,
        ),
    ]
