# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_auto_20150727_2116'),
    ]

    operations = [
        migrations.CreateModel(
            name='DuplicateGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(null=True, blank=True)),
                ('child', models.ForeignKey(related_name='group_children', blank=True, to='api.Group', null=True)),
                ('parent', models.ForeignKey(related_name='group_duplicates', to='api.Group')),
            ],
        ),
        migrations.RemoveField(
            model_name='groupf',
            name='child',
        ),
        migrations.RemoveField(
            model_name='groupf',
            name='parent',
        ),
        migrations.DeleteModel(
            name='GroupF',
        ),
    ]
