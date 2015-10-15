# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0055_auto_20151015_1613'),
    ]

    operations = [
        migrations.RenameField(
            model_name='catalog',
            old_name='arranger',
            new_name='person',
        ),
        migrations.AlterUniqueTogether(
            name='catalog',
            unique_together=set([('person', 'song')]),
        ),
    ]
