# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.api.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20151013_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.  Must be unique.  If there are singer name conflicts, please add middle initial, nickname, or other identifying information.', unique=True, max_length=200, validators=[apps.api.validators.validate_trimmed]),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.  Must be unique.  If there are singer name conflicts, please add middle initial, nickname, or other identifying information.', unique=True, max_length=200, validators=[apps.api.validators.validate_trimmed]),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.  Must be unique.  If there are singer name conflicts, please add middle initial, nickname, or other identifying information.', unique=True, max_length=200, validators=[apps.api.validators.validate_trimmed]),
        ),
    ]
