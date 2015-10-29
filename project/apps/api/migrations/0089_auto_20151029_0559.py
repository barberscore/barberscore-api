# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0088_auto_20151029_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='goal',
            field=models.IntegerField(help_text=b'\n            The objective of the contest', choices=[(1, b'Championship'), (2, b'Prelims')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='panel',
            field=models.IntegerField(help_text=b'\n            Size of the judging panel (typically three or five.)', choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='rounds',
            field=models.IntegerField(help_text=b'\n            Bracket size', choices=[(3, 3), (2, 2), (1, 1)]),
        ),
    ]
