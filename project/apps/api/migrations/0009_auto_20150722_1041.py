# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20150722_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arranger',
            name='person',
            field=models.ForeignKey(related_name='arrangements', to='api.Person'),
        ),
    ]
