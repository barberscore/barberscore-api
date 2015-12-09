# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20151208_2359'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contest',
            old_name='contest_id',
            new_name='subsession_id',
        ),
    ]
