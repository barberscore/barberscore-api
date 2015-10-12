# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20151009_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='is_active',
        ),
        migrations.AddField(
            model_name='district',
            name='end_date',
            field=models.DateField(help_text=b'\n            The closing/deceased date of the resource.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='district',
            name='start_date',
            field=models.DateField(help_text=b'\n            The founding/birth date of the resource.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='end_date',
            field=models.DateField(help_text=b'\n            The closing/deceased date of the resource.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='start_date',
            field=models.DateField(help_text=b'\n            The founding/birth date of the resource.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='end_date',
            field=models.DateField(help_text=b'\n            The closing/deceased date of the resource.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='start_date',
            field=models.DateField(help_text=b'\n            The founding/birth date of the resource.', null=True, blank=True),
        ),
    ]
