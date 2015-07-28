# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_auto_20150727_2103'),
    ]

    operations = [
        migrations.RenameModel('Spot', 'Arrangement')
    ]
