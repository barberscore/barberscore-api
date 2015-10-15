# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_auto_20151015_0918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slot',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='contestant',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='draw',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='stagetime',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='draw',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='stagetime',
        ),
        migrations.AlterField(
            model_name='performance',
            name='contest',
            field=models.ForeignKey(related_name='performances', to='api.Contest'),
        ),
        migrations.AlterField(
            model_name='performance',
            name='contestant',
            field=models.ForeignKey(related_name='performances', to='api.Contestant'),
        ),
        migrations.DeleteModel(
            name='Slot',
        ),
    ]
