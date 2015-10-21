# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_session_slots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='rounds',
            field=models.IntegerField(default=5, help_text=b'\n            Bracket size', choices=[(3, 3), (2, 2), (1, 1)]),
        ),
        migrations.AlterUniqueTogether(
            name='appearance',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='appearance',
            name='kind',
        ),
    ]
