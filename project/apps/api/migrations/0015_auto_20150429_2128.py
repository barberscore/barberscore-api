# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20150429_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(related_name='contests', to='api.Convention'),
        ),
    ]
