# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0012_auto_20140610_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='contestants',
        ),
        migrations.AlterField(
            model_name='performance',
            name='contest_round',
            field=models.IntegerField(default=0, editable=False, choices=[(1, b'Quarter-Finals'), (2, b'Semi-Finals'), (3, b'Finals')]),
        ),
    ]
