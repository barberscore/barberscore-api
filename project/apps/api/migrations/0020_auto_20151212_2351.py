# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
import apps.api.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20151212_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='awards', to='api.Organization'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the resource.', max_length=200, validators=[apps.api.validators.validate_trimmed]),
        ),
    ]
