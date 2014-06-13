# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0021_auto_20140613_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='session',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Morning'), (2, b'Evening')]),
            preserve_default=True,
        ),
    ]
