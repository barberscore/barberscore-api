# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_contest_round'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contest',
            old_name='qual_score',
            new_name='cutoff',
        ),
    ]
