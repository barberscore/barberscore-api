# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20151207_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='stix_file',
            field=models.FileField(help_text=b'\n            The bbstix file.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
    ]
