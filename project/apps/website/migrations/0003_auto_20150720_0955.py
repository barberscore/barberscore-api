# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20150720_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='primitive',
            field=models.ForeignKey(related_name='collections', to='website.Primitive'),
        ),
    ]
