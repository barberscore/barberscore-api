# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20150126_1025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='singer',
            options={'ordering': ('name',)},
        ),
        migrations.RemoveField(
            model_name='chorus',
            name='district',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='district',
        ),
        migrations.AddField(
            model_name='chorus',
            name='men',
            field=models.IntegerField(help_text=b'\n            The number of men on stage.', null=True, blank=True),
            preserve_default=True,
        ),
    ]
