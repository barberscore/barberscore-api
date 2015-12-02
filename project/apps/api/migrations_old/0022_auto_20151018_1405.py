# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20151018_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='men',
            field=models.IntegerField(default=4, help_text=b'\n            The number of men on stage (only for chourses).'),
        ),
    ]
