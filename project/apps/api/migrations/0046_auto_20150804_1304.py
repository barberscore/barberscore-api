# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_auto_20150729_1138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='singer',
            options={'ordering': ('-name',)},
        ),
    ]
