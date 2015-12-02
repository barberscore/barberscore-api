# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0099_auto_20151105_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='organization',
            field=models.ForeignKey(blank=True, to='api.Organization', null=True),
        ),
    ]
