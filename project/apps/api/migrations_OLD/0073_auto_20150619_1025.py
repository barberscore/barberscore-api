# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0072_auto_20150619_0951'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contest',
            unique_together=set([]),
        ),
    ]
