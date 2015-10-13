# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20151013_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='year',
            field=models.IntegerField(default=2015, validators=[django.core.validators.MaxValueValidator(2016, message=b'Year must be between 1939 and 2016'), django.core.validators.MinValueValidator(1938, message=b'Year must be between 1939 and 2016')]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='year',
            field=models.IntegerField(default=2015, validators=[django.core.validators.MaxValueValidator(2016, message=b'Year must be between 1939 and 2016'), django.core.validators.MinValueValidator(1938, message=b'Year must be between 1939 and 2016')]),
        ),
    ]
