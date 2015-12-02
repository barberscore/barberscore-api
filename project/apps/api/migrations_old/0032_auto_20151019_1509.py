# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_auto_20151019_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='kind',
            field=models.IntegerField(default=1, choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='level',
            field=models.IntegerField(default=1, choices=[(1, b'International'), (2, b'District'), (3, b'Division')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='rounds',
            field=models.IntegerField(default=5, help_text=b'\n            Bracket size', choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]),
        ),
    ]
