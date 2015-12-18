# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_auto_20151217_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='award',
            field=models.ForeignKey(related_name='contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Award', null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The kind of session.  Generally this will be either quartet or chorus, with the exception being International and Midwinter which hold exclusive Collegiate and Senior sessions respectively.', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Seniors Quartet'), (4, b'Collegiate Quartet'), (5, b'Novice Quartet')]),
        ),
    ]
