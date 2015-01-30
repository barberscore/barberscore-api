# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_auto_20150129_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='district',
        ),
        migrations.RemoveField(
            model_name='chorus',
            name='chapter',
        ),
        migrations.RemoveField(
            model_name='singer',
            name='chapter',
        ),
        migrations.DeleteModel(
            name='Chapter',
        ),
        migrations.AddField(
            model_name='chorus',
            name='chapter_code',
            field=models.CharField(help_text=b'\n            The code of the director(s) of the chorus.', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chorus',
            name='chapter_name',
            field=models.CharField(help_text=b'\n            The name of the director(s) of the chorus.', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chorus',
            name='district',
            field=models.ForeignKey(blank=True, to='api.District', null=True),
            preserve_default=True,
        ),
    ]
