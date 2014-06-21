# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0042_auto_20140620_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='total_score',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='song2_score',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='performance_score',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='song1_score',
        ),
    ]
