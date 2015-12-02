# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_auto_20151020_0821'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appearance',
            options={'ordering': ['position']},
        ),
    ]
