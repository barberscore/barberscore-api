# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0005_auto_20140521_0544'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='location',
        ),
        migrations.RemoveField(
            model_name='contest',
            name=b'panel_size',
        ),
    ]
