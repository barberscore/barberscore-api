# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_auto_20150129_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='panel',
            field=models.IntegerField(default=5, help_text=b'\n            Size of the judging panel (typically\n            three or five.)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contest',
            name='scoresheet',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
