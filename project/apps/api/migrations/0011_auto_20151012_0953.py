# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20151012_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='is_active',
            field=models.BooleanField(default=False, help_text=b'\n            A boolean for active/living resources.'),
        ),
        migrations.AlterField(
            model_name='district',
            name='long_name',
            field=models.CharField(help_text=b'\n            A long-form name for the resource.', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='is_active',
            field=models.BooleanField(default=False, help_text=b'\n            A boolean for active/living resources.'),
        ),
        migrations.AlterField(
            model_name='person',
            name='is_active',
            field=models.BooleanField(default=False, help_text=b'\n            A boolean for active/living resources.'),
        ),
    ]
