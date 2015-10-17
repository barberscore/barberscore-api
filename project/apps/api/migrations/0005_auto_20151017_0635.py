# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20151017_0445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='district',
            field=models.ForeignKey(related_name='contests', to='api.District'),
        ),
    ]
