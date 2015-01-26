# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20150126_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chorus',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='district',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartet',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='singer',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
            preserve_default=True,
        ),
    ]
