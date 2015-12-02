# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0087_auto_20151028_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='goal',
            field=models.IntegerField(default=1, help_text=b'\n            The objective of the contest'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='kind',
            field=models.IntegerField(choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='level',
            field=models.IntegerField(choices=[(1, b'International'), (2, b'District'), (3, b'Division')]),
        ),
    ]
