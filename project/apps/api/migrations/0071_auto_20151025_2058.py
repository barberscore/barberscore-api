# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0070_auto_20151025_2055'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ['performance', 'order']},
        ),
        migrations.AlterField(
            model_name='performance',
            name='contestant',
            field=models.ForeignKey(related_name='performances', to='api.Contestant'),
        ),
        migrations.AlterField(
            model_name='performance',
            name='session',
            field=models.ForeignKey(related_name='performances', to='api.Session'),
        ),
    ]
