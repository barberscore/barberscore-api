# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20150124_2055'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='district',
            options={'ordering': ['kind', 'name']},
        ),
        migrations.AddField(
            model_name='chorus',
            name='chapter',
            field=models.OneToOneField(null=True, blank=True, to='api.Chapter'),
            preserve_default=True,
        ),
    ]
