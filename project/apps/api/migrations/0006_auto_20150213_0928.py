# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20150208_1015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='csv_finals',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='csv_quarters',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='csv_semis',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='scoresheet',
        ),
        migrations.AddField(
            model_name='contest',
            name='scoresheet_csv',
            field=models.FileField(null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
        migrations.AddField(
            model_name='contest',
            name='scoresheet_pdf',
            field=models.FileField(null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
    ]
