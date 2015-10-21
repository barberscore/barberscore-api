# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_auto_20151021_0920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='rep',
        ),
        migrations.AlterField(
            model_name='arranger',
            name='performance',
            field=models.ForeignKey(related_name='arrangers', to='api.Performance'),
        ),
        migrations.AlterField(
            model_name='arranger',
            name='person',
            field=models.ForeignKey(related_name='arrangements', to='api.Person'),
        ),
    ]
