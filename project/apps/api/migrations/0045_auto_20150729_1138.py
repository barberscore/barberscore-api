# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_auto_20150728_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singer',
            name='part',
            field=models.IntegerField(choices=[(1, b'Tenor'), (2, b'Lead'), (3, b'Baritone'), (4, b'Bass')]),
        ),
    ]
