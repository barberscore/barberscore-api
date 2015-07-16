# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0074_auto_20150619_1104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contest',
            old_name='district_fk',
            new_name='district',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='district_fk',
            new_name='district',
        ),
    ]
