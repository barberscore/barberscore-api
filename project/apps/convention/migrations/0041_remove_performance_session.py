# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0040_auto_20140620_1338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='session',
        ),
    ]
