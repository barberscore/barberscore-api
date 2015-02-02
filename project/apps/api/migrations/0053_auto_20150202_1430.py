# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_auto_20150201_2139'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contest',
            old_name='scoresheet_csv',
            new_name='csv_q1',
        ),
    ]
