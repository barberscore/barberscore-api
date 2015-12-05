# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_auto_20151204_2121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ('session', 'position')},
        ),
        migrations.AlterField(
            model_name='session',
            name='name',
            field=models.CharField(unique=True, max_length=255, editable=False),
        ),
    ]
