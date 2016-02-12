# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0116_auto_20160212_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='administrator',
            field=models.ForeignKey(related_name='sessions', blank=True, to='api.Person', null=True),
        ),
    ]
