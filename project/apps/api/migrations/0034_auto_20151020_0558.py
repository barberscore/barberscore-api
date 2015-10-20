# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20151020_0554'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b'New'), (1, b'Structured'), (2, b'Current'), (3, b'Complete')])),
                ('status_monitor', model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status')),
                ('kind', models.IntegerField(default=1, choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')])),
                ('start', models.DateTimeField(null=True, blank=True)),
                ('contest', models.ForeignKey(related_name='sessions', to='api.Contest')),
            ],
            options={
                'ordering': ['contest', 'kind'],
            },
        ),
        migrations.AlterModelOptions(
            name='appearance',
            options={'ordering': ['session', 'draw', 'contestant']},
        ),
        migrations.AddField(
            model_name='appearance',
            name='contest',
            field=models.ForeignKey(related_name='appearances', blank=True, to='api.Contest', null=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='contestant',
            field=models.ForeignKey(related_name='appearances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Contestant', null=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='draw',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='kind',
            field=models.IntegerField(null=True, choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')]),
        ),
        migrations.AddField(
            model_name='appearance',
            name='session',
            field=models.ForeignKey(related_name='appearances', blank=True, to='api.Session', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([('contest', 'kind')]),
        ),
    ]
