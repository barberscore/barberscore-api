# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20150429_2128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['-contest', 'round', 'queue', 'group']},
        ),
        migrations.AlterField(
            model_name='groupfinish',
            name='contest',
            field=models.ForeignKey(to='api.Contest'),
        ),
        migrations.AlterField(
            model_name='groupfinish',
            name='group',
            field=models.ForeignKey(related_name='finishes', to='api.Group'),
        ),
    ]
