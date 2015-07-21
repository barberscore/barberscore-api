# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_primitive_trainer'),
    ]

    operations = [
        migrations.AddField(
            model_name='primitive',
            name='training_file',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
    ]
