# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20151013_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='district',
            field=models.ForeignKey(help_text=b"\n            The district for the convention.  If International, this is 'BHS'.", to='api.District'),
        ),
    ]
