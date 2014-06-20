# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0037_auto_20140619_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='ordinal',
            field=models.IntegerField(default=1, help_text=b'\n            The session number.', choices=[(1, b'Session #1'), (2, b'Session #2')]),
            preserve_default=True,
        ),
    ]
