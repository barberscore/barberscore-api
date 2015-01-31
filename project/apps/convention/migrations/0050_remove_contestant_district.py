# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0049_auto_20140701_0908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name=b'district',
        ),
    ]
