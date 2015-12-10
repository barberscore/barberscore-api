# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.api.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_auto_20151209_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', max_length=200, editable=False, validators=[apps.api.validators.validate_trimmed]),
        ),
    ]
