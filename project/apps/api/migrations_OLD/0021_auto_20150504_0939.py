# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20150504_0926'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['round']},
        ),
        migrations.RemoveField(
            model_name='performance',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='group',
        ),
        migrations.AlterField(
            model_name='performance',
            name='appearance',
            field=models.ForeignKey(to='api.Appearance'),
        ),
    ]
