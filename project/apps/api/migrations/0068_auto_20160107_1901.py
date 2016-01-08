# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0067_auto_20160106_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The kind of session.  Generally this will be either quartet or chorus, with the exception being International and Midwinter which hold exclusive Collegiate and Senior sessions respectively.', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Seniors'), (4, b'Collegiate'), (5, b'Novice')]),
        ),
    ]
