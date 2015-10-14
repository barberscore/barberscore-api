# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20151013_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='name',
            field=models.CharField(default=datetime.datetime(2015, 10, 14, 4, 44, 28, 819759, tzinfo=utc), unique=True, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='score',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=datetime.datetime(2015, 10, 14, 4, 44, 41, 507484, tzinfo=utc), editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True),
            preserve_default=False,
        ),
    ]
