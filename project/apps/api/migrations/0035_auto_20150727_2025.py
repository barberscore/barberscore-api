# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20150727_2002'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='arranger',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='arranger',
            name='catalog',
        ),
        migrations.RemoveField(
            model_name='arranger',
            name='chart',
        ),
        migrations.RemoveField(
            model_name='arranger',
            name='person',
        ),
        migrations.RemoveField(
            model_name='catalog',
            name='person',
        ),
        migrations.RemoveField(
            model_name='catalog',
            name='song',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='catalog',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='chart',
        ),
        migrations.AlterField(
            model_name='spot',
            name='arranger',
            field=models.ForeignKey(related_name='arrangements', blank=True, to='api.Person', null=True),
        ),
        migrations.DeleteModel(
            name='Arranger',
        ),
        migrations.DeleteModel(
            name='Catalog',
        ),
    ]
