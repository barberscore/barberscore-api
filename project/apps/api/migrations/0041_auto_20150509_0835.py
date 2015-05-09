# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_auto_20150509_0829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='district_tag',
            new_name='district',
        ),
    ]
