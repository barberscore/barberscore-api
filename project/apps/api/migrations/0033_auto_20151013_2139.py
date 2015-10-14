# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_auto_20151013_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='judge',
            field=models.ForeignKey(related_name='scores', to='api.Judge'),
        ),
        migrations.AlterField(
            model_name='score',
            name='performance',
            field=models.ForeignKey(related_name='scores', to='api.Performance'),
        ),
        migrations.AlterField(
            model_name='score',
            name='points',
            field=models.IntegerField(help_text=b'\n            The number of points awarded (0-100)', validators=[django.core.validators.MaxValueValidator(100, message=b'Points must be between 0 - 100'), django.core.validators.MinValueValidator(0, message=b'Points must be between 0 - 100')]),
        ),
    ]
