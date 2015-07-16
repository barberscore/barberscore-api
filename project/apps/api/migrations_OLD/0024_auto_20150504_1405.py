# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20150504_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('seed', models.IntegerField(null=True, blank=True)),
                ('prelim', models.FloatField(null=True, blank=True)),
                ('place', models.IntegerField(null=True, blank=True)),
                ('score', models.FloatField(null=True, blank=True)),
                ('contest', models.ForeignKey(related_name='contestants', to='api.Contest')),
                ('group', models.ForeignKey(related_name='contestants', to='api.Group')),
            ],
            options={
                'ordering': ('contest', 'group', 'place', 'seed'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='appearance',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='appearance',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='appearance',
            name='group',
        ),
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['contestant', 'round', 'queue']},
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='performance',
            name='appearance',
        ),
        migrations.AddField(
            model_name='performance',
            name='contestant',
            field=models.ForeignKey(related_name='performances', blank=True, to='api.Contestant', null=True),
        ),
        migrations.DeleteModel(
            name='Appearance',
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('group', 'contest')]),
        ),
    ]
