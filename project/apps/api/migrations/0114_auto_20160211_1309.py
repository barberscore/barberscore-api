# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0113_auto_20160211_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='drcj',
            field=models.ForeignKey(related_name='conventions', blank=True, to='api.Person', help_text=b'\n            The person managing the convention.', null=True),
        ),
    ]
