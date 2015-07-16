# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0143_auto_20150708_0507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='director',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='singer',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True),
        ),
    ]
