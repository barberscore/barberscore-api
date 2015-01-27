# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20150126_1141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chorus',
            name='men',
        ),
        migrations.AddField(
            model_name='chorusperformance',
            name='men',
            field=models.IntegerField(help_text=b'\n            The number of men on stage.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contest',
            name='year',
            field=models.IntegerField(default=2015, max_length=4, choices=[(2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)]),
            preserve_default=True,
        ),
    ]
