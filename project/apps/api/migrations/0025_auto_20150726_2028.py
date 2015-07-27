# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20150726_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='primitive',
        ),
        migrations.RemoveField(
            model_name='duplicate',
            name='collection',
        ),
        migrations.DeleteModel(
            name='Collection',
        ),
        migrations.DeleteModel(
            name='Duplicate',
        ),
        migrations.DeleteModel(
            name='Primitive',
        ),
    ]
