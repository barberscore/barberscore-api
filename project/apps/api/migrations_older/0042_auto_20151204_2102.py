# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_auto_20151204_2055'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='judge',
            options={'ordering': ('contest', 'kind', 'category', 'slot')},
        ),
        migrations.AlterField(
            model_name='score',
            name='name',
            field=models.CharField(unique=True, max_length=255, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='judge',
            unique_together=set([('contest', 'kind', 'category', 'slot')]),
        ),
    ]
