# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django.utils.timezone
import model_utils.fields
import django_fsm
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0125_session_performance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('status', django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (40, b'Confirmed'), (50, b'Final')])),
                ('status_monitor', model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status')),
                ('place', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ['session', 'place'],
            },
        ),
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['position']},
        ),
        migrations.AddField(
            model_name='rank',
            name='performance',
            field=models.ForeignKey(related_name='ranks', to='api.Performance'),
        ),
        migrations.AddField(
            model_name='rank',
            name='session',
            field=models.ForeignKey(related_name='ranks', to='api.Session'),
        ),
        migrations.AlterUniqueTogether(
            name='rank',
            unique_together=set([('session', 'performance')]),
        ),
    ]
