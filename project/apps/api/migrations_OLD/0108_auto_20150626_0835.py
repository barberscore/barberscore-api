# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0107_auto_20150626_0037'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['contestant', 'round', 'draw', 'stagetime']},
        ),
        migrations.RenameField(
            model_name='contestant',
            old_name='queue',
            new_name='draw',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='queue',
            new_name='draw',
        ),
    ]
