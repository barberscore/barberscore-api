# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20151201_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='convention',
            field=models.ForeignKey(related_name='contestants', to='api.Convention'),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='contestants', blank=True, to='api.Organization', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('group', 'convention')]),
        ),
    ]
