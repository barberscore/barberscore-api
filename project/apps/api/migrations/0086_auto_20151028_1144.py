# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0085_auto_20151027_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='organization',
            field=models.ForeignKey(related_name='contests', to='api.Organization'),
        ),
    ]
