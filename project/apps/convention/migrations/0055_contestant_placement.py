# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0054_contest_panel'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='placement',
            field=models.IntegerField(help_text=b'Final placement', null=True, blank=True),
            preserve_default=True,
        ),
    ]
