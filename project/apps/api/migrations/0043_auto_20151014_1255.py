# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_auto_20151014_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=1, editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='award',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set([('kind', 'contestant')]),
        ),
    ]
