# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_auto_20150508_1400'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='district',
            new_name='district_OLD',
        ),
    ]
