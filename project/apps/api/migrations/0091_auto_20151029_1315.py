# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0090_auto_20151029_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the contest (determined programmatically.)', unique=True, max_length=200, editable=False),
        ),
    ]
