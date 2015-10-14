# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_auto_20151014_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='judge',
            name='num',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='judge',
            unique_together=set([('contest', 'part', 'num')]),
        ),
    ]
