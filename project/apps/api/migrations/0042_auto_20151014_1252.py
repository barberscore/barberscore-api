# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_auto_20151014_1120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='judge',
            options={'ordering': ('contest', 'part', 'num')},
        ),
        migrations.AddField(
            model_name='award',
            name='kind',
            field=models.IntegerField(default=1, choices=[(1, b'First Place Gold Medalist'), (2, b'Second Place Silver Medalist'), (3, b'Third Place Bronze Medalist'), (4, b'Fourth Place Bronze Medalist'), (5, b'Fifth Place Bronze Medalist')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='award',
            name='name',
            field=models.IntegerField(choices=[(1, b'First Place Gold Medalist'), (2, b'Second Place Silver Medalist'), (3, b'Third Place Bronze Medalist'), (4, b'Fourth Place Bronze Medalist'), (5, b'Fifth Place Bronze Medalist')]),
        ),
    ]
