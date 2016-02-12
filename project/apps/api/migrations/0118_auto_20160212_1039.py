# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0117_session_administrator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge',
            name='category',
            field=models.IntegerField(choices=[(1, b'Music'), (2, b'Presentation'), (3, b'Singing')]),
        ),
    ]
