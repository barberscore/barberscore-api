# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0008_auto_20140521_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='contest_round',
            field=models.IntegerField(default=0, choices=[(1, b'Quarter-Finals'), (2, b'Semi-Finals'), (3, b'Finals')]),
            preserve_default=True,
        ),
    ]
