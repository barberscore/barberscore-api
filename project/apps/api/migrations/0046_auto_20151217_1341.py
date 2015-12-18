# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_auto_20151217_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='kind',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Seniors Quartet'), (4, b'Collegiate Quartet'), (5, b'Novice Quartet')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The kind of session.  Generally this will be either quartet or chorus, with the exception being International and Midwinter which hold exclusive Collegiate and Senior sessions respectively.', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Seniors Quartet'), (4, b'Collegiate Quartet'), (4, b'Novice Quartet')]),
        ),
    ]
