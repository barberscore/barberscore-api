# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_award_rounds'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set([('organization', 'long_name', 'kind')]),
        ),
    ]
