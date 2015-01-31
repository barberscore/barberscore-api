# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0041_remove_performance_session'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance',
            old_name='ordinal',
            new_name='session',
        ),
    ]
