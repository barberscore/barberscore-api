# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0025_contestant_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='slug',
        ),
    ]
