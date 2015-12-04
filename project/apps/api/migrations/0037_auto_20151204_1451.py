# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20151204_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge',
            name='kind',
            field=models.IntegerField(choices=[(0, b'Admin'), (1, b'Music'), (2, b'Presentation'), (3, b'Singing')]),
        ),
        migrations.AlterField(
            model_name='score',
            name='judge',
            field=models.ForeignKey(related_name='scores', to='api.Judge'),
        ),
        migrations.AlterField(
            model_name='score',
            name='kind',
            field=models.IntegerField(choices=[(0, b'Admin'), (1, b'Music'), (2, b'Presentation'), (3, b'Singing')]),
        ),
    ]
