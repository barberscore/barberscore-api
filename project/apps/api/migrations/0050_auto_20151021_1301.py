# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_auto_20151021_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appearance',
            name='contest',
        ),
        migrations.AlterField(
            model_name='appearance',
            name='contestant',
            field=models.ForeignKey(related_name='appearances', to='api.Contestant'),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='position',
            field=models.PositiveSmallIntegerField(verbose_name=b'Position'),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='session',
            field=models.ForeignKey(related_name='appearances', to='api.Session'),
        ),
    ]
