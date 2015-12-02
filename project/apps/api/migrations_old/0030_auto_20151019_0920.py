# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20151019_0556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='bracket',
        ),
        migrations.AddField(
            model_name='contest',
            name='rounds',
            field=models.IntegerField(default=1, help_text=b'\n            Bracket size', choices=[(1, b'One'), (2, b'Two'), (3, b'Three')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='level',
            field=models.IntegerField(default=1, help_text=b'\n            The level of the contest (currently only International is supported.)', choices=[(1, b'International'), (2, b'District'), (3, b'Division')]),
        ),
    ]
