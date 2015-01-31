# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0003_auto_20140507_0752'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='contest_type2',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Quartet Contest'), (2, b'Chorus Contest'), (3, b'Collegiate Contest'), (4, b'Senior Contest')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contest',
            name='location',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='contest',
            name=b'contest_type',
        ),
        migrations.RemoveField(
            model_name='contest',
            name=b'contest_level',
        ),
        migrations.RemoveField(
            model_name='contest',
            name=b'year',
        ),
    ]
