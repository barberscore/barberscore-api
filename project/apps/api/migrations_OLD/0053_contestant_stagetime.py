# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_auto_20150518_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='stagetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
