# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0004_auto_20140521_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='contest_type',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Quartet Contest'), (2, b'Chorus Contest'), (3, b'Collegiate Contest'), (4, b'Senior Contest')]),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='contest',
            name='contest_type2',
        ),
    ]
