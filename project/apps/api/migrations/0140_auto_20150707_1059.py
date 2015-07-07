# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0139_arranger'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arranger',
            name='contestant',
        ),
        migrations.RemoveField(
            model_name='arranger',
            name='person',
        ),
        migrations.DeleteModel(
            name='Arranger',
        ),
    ]
