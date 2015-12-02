# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20151201_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panel',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The Panel is different than the contest objective.', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate')]),
        ),
        migrations.AlterField(
            model_name='panel',
            name='rounds',
            field=models.IntegerField(help_text=b'\n            Number of rounds', choices=[(3, 3), (2, 2), (1, 1)]),
        ),
        migrations.AlterField(
            model_name='panel',
            name='size',
            field=models.IntegerField(help_text=b'\n            Size of the judging panel (typically three or five.)', choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]),
        ),
    ]
