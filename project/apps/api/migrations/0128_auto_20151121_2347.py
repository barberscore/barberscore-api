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
        ('api', '0127_remove_session_performance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('status', django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (25, b'Finished'), (30, b'Final')])),
                ('status_monitor', model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status')),
                ('kind', models.IntegerField(choices=[(1, b'Sunday'), (2, b'Monday'), (3, b'Tuesday'), (4, b'Wednesday'), (5, b'Thursday'), (6, b'Friday'), (7, b'Saturday')])),
                ('start_date', models.DateField(null=True, blank=True)),
                ('convention', models.ForeignKey(related_name='days', to='api.Convention')),
            ],
            options={
                'ordering': ['convention', 'kind'],
            },
        ),
        migrations.AddField(
            model_name='performance',
            name='day',
            field=models.ForeignKey(related_name='performances', blank=True, to='api.Day', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='day',
            unique_together=set([('convention', 'kind')]),
        ),
    ]
