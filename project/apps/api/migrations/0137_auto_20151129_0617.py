# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0136_auto_20151129_0539'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='contest',
            field=models.ForeignKey(related_name='days', blank=True, to='api.Contest', null=True),
        ),
        migrations.AlterField(
            model_name='award',
            name='kind',
            field=models.IntegerField(choices=[(1, b'Championship'), (2, b'Qualifier'), (3, b'Novice')]),
        ),
        migrations.AlterField(
            model_name='day',
            name='kind',
            field=models.IntegerField(choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')]),
        ),
    ]
