# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0052_auto_20140701_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='running_total',
            field=models.FloatField(help_text=b'Average score across contests', null=True, blank=True),
            preserve_default=True,
        ),
    ]
