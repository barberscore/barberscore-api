# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20150124_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='code',
            field=models.CharField(help_text=b'\n            The Chapter code', max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the chapter.', max_length=200),
            preserve_default=True,
        ),
    ]
