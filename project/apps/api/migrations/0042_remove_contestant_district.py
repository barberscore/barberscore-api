# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_auto_20150509_0835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name='district',
        ),
    ]
