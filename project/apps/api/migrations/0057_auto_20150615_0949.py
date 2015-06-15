# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import apps.api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0056_auto_20150521_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=apps.api.models.populate_contest, always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=apps.api.models.populate_contestant, always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='district',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=apps.api.models.populate_performance, always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='singer',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
    ]
