# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_auto_20151014_1002'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='judge',
            unique_together=set([]),
        ),
    ]
