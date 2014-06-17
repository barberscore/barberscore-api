# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0034_auto_20140617_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='startdate',
        ),
    ]
