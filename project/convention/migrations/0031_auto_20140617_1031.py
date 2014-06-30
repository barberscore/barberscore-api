# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0030_auto_20140616_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='contestant_type',
            field=models.IntegerField(default=1, help_text=b'\n            The type of contestant, either chorus or quartet.', choices=[(1, b'Quartet'), (2, b'Chorus')]),
        ),
    ]
