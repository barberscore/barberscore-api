# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_auto_20151015_1226'),
    ]

    operations = [
        migrations.RenameModel('Arrangement', 'Catalog'),
    ]
