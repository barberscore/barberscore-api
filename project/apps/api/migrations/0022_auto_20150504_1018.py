# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20150504_0939'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appearance',
            options={'ordering': ('contest', 'group', 'place', 'seed')},
        ),
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['appearance', 'round', 'queue']},
        ),
        migrations.AlterField(
            model_name='appearance',
            name='contest',
            field=models.ForeignKey(related_name='appearances', to='api.Contest'),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='group',
            field=models.ForeignKey(related_name='appearances', to='api.Group'),
        ),
        migrations.AlterField(
            model_name='performance',
            name='appearance',
            field=models.ForeignKey(related_name='performances', to='api.Appearance'),
        ),
        migrations.AlterUniqueTogether(
            name='appearance',
            unique_together=set([('group', 'contest')]),
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('appearance', 'round', 'queue')]),
        ),
    ]
