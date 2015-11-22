# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0129_auto_20151122_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='entrant',
            field=models.ForeignKey(related_name='performances', blank=True, to='api.Entrant', null=True),
        ),
    ]
