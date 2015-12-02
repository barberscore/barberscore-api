# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0097_auto_20151103_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='song',
            field=models.ForeignKey(related_name='scores', to='api.Song'),
        ),
    ]
