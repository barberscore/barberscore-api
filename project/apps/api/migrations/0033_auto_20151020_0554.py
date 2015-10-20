# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_auto_20151019_1509'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appearance',
            options={'ordering': ['contestant', 'kind']},
        ),
        migrations.RenameField(
            model_name='appearance',
            old_name='session',
            new_name='kind',
        ),
        migrations.AlterUniqueTogether(
            name='appearance',
            unique_together=set([('contestant', 'kind')]),
        ),
    ]
