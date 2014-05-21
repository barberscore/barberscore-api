# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'bbs', b'0002_contest_contestant_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name=b'contestant',
            name=b'district',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name=b'contestant',
            name=b'contestant_type',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Quartet'), (2, b'Chorus')]),
        ),
    ]
