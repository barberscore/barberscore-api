# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0020_auto_20140613_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='total_score',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='performance',
            name='place',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='seed',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='rank',
        ),
    ]
