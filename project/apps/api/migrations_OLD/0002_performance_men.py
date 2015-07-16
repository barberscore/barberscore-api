# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='men',
            field=models.IntegerField(help_text=b'\n            Men on stage.', null=True, blank=True),
        ),
    ]
