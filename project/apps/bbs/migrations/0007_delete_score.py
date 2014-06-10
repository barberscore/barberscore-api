# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0006_auto_20140521_0549'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Score',
        ),
    ]
