# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import apps.api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_auto_20151020_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='district',
            field=models.ForeignKey(related_name='contestants', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='men',
            field=models.IntegerField(default=4, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='picture',
            field=models.ImageField(null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='place',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='prelim',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='seed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='start',
            field=models.DateField(null=True, blank=True),
        ),
    ]
