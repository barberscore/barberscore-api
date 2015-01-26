# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20150126_1047'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chorus',
            options={'verbose_name_plural': 'choruses'},
        ),
        migrations.AlterModelOptions(
            name='quartet',
            options={'ordering': ('name',)},
        ),
    ]
