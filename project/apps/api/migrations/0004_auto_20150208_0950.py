# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20150205_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='men',
            field=models.IntegerField(default=4, help_text=b'\n            Men on stage.', null=True, blank=True),
        ),
    ]
