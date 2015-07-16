# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0058_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='performance',
            field=models.ForeignKey(to='api.Performance'),
        ),
    ]
