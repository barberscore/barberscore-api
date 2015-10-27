# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0075_auto_20151027_1239'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='arranger',
            unique_together=set([('catalog', 'person')]),
        ),
        migrations.RemoveField(
            model_name='arranger',
            name='song',
        ),
    ]
