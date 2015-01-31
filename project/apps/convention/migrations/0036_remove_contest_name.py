# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0035_remove_contest_startdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='name',
        ),
    ]
