# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0018_auto_20140612_2157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name='website2',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='facebook2',
        ),
    ]
