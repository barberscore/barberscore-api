# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_auto_20150202_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='csv_f1',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contest',
            name='csv_q2',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contest',
            name='csv_q3',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contest',
            name='csv_s1',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contest',
            name='csv_s2',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
