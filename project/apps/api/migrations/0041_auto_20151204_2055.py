# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_auto_20151204_1502'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='score',
            options={'ordering': ('judge', 'song')},
        ),
        migrations.AlterField(
            model_name='score',
            name='points',
            field=models.IntegerField(blank=True, help_text=b'\n            The number of points awarded (0-100)', null=True, validators=[django.core.validators.MaxValueValidator(100, message=b'Points must be between 0 - 100'), django.core.validators.MinValueValidator(0, message=b'Points must be between 0 - 100')]),
        ),
    ]
