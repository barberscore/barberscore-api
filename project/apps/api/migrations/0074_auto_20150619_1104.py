# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0073_auto_20150619_1025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contest',
            options={'ordering': ('level', 'kind', '-year')},
        ),
        migrations.RemoveField(
            model_name='contest',
            name='district',
        ),
        migrations.RemoveField(
            model_name='group',
            name='district',
        ),
    ]
