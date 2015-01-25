# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='district',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='district',
            name='kind',
            field=models.IntegerField(default=1, choices=[(1, b'District'), (2, b'Affiliate')]),
            preserve_default=True,
        ),
    ]
