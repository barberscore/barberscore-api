# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0112_auto_20160206_1550'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='organization',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='convention',
            name='drcj',
            field=models.ForeignKey(related_name='conventions', blank=True, to='api.Organization', help_text=b'\n            The person managing the convention.', null=True),
        ),
    ]
