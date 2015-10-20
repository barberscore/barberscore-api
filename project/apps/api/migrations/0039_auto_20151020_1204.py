# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_auto_20151020_0823'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='judge',
            options={'ordering': ('contest', 'category', 'num')},
        ),
        migrations.AddField(
            model_name='judge',
            name='category',
            field=models.IntegerField(null=True, choices=[(0, b'Administator'), (1, b'Music'), (2, b'Presentation'), (3, b'Singing'), (4, b'Administrator'), (5, b'Music (Practice)'), (6, b'Presenation (Practice)'), (7, b'Singing (Practice)')]),
        ),
        migrations.AlterUniqueTogether(
            name='judge',
            unique_together=set([('contest', 'category', 'num')]),
        ),
        migrations.RemoveField(
            model_name='judge',
            name='part',
        ),
    ]
