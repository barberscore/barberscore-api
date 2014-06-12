# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0009_performance_contest_round'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='appearance',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
