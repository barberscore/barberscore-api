# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_auto_20150129_2103'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contest',
            options={'ordering': ['convention__district', 'kind', 'convention__year']},
        ),
        migrations.RemoveField(
            model_name='contest',
            name='district',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='level',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='year',
        ),
        migrations.AddField(
            model_name='contest',
            name='slug',
            field=autoslug.fields.AutoSlugField(null=True, editable=False, blank=True, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(default=1, choices=[(1, b'Summer'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='convention',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, editable=False),
            preserve_default=True,
        ),
    ]
