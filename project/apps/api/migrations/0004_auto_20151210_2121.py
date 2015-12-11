# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_performance_convention'),
    ]

    operations = [
        migrations.RenameField(
            model_name='convention',
            old_name='kind',
            new_name='season',
        ),
        migrations.AlterUniqueTogether(
            name='convention',
            unique_together=set([('organization', 'season', 'year')]),
        ),
    ]
