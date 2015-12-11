# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20151210_2243'),
    ]

    operations = [
        migrations.RenameField(
            model_name='convention',
            old_name='season',
            new_name='kind',
        ),
        migrations.AlterUniqueTogether(
            name='convention',
            unique_together=set([('organization', 'kind', 'year', 'combo')]),
        ),
    ]
