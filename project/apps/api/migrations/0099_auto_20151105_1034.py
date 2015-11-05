# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0098_auto_20151104_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='arranger',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='name',
            field=models.CharField(unique=True, max_length=255, editable=False),
        ),
        migrations.AlterField(
            model_name='song',
            name='performance',
            field=models.ForeignKey(related_name='songs', to='api.Performance'),
        ),
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
