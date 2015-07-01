# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0115_auto_20150701_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
    ]
