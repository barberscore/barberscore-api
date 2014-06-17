# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0033_auto_20140617_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='year',
            field=models.CharField(default=b'2014', help_text=b'\n            The year of the contest, as a Char.', max_length=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contest',
            name='contest_level',
            field=models.IntegerField(default=1, help_text=b'\n            The contest level:  International, District, etc..\n            Currently only International is supported.', choices=[(1, b'International')]),
        ),
    ]
