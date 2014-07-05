# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0055_contestant_placement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contestant',
            old_name='placement',
            new_name='place',
        ),
        migrations.AlterField(
            model_name='performance',
            name='place',
            field=models.IntegerField(help_text=b'\n            The ordinal placement of this performance in this\n            particular contest round.', null=True, blank=True),
        ),
    ]
