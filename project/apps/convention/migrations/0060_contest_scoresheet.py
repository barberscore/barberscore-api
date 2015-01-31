# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0059_auto_20140705_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='scoresheet',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
