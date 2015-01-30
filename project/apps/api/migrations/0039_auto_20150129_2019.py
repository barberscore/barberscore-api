# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_auto_20150129_0839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chorus',
            name='blurb',
        ),
        migrations.RemoveField(
            model_name='district',
            name='blurb',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='blurb',
        ),
        migrations.RemoveField(
            model_name='singer',
            name='blurb',
        ),
        migrations.AddField(
            model_name='chorus',
            name='description',
            field=models.TextField(help_text=b'\n            A description/bio of the resource.  Max 1000 characters.', max_length=1000, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='district',
            name='description',
            field=models.TextField(help_text=b'\n            A description/bio of the resource.  Max 1000 characters.', max_length=1000, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartet',
            name='description',
            field=models.TextField(help_text=b'\n            A description/bio of the resource.  Max 1000 characters.', max_length=1000, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='singer',
            name='description',
            field=models.TextField(help_text=b'\n            A description/bio of the resource.  Max 1000 characters.', max_length=1000, blank=True),
            preserve_default=True,
        ),
    ]
