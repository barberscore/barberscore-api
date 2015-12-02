# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_remove_score_is_practice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('-contest__year', 'place')},
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='score',
        ),
    ]
