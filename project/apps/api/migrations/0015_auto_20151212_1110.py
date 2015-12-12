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
        ('api', '0014_auto_20151212_1020'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, editable=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('status', django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Active'), (20, b'Inactive')])),
                ('status_monitor', model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status')),
                ('kind', models.IntegerField(choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate'), (4, b'Novice')])),
                ('long_name', models.CharField(unique=True, max_length=200)),
                ('is_championship', models.BooleanField(default=True, help_text=b'\n            Championships are awards with only one winner.')),
                ('organization', models.ForeignKey(related_name='awards', to='api.Organization')),
            ],
            options={
                'ordering': ('organization', 'kind'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set([('organization', 'long_name', 'kind')]),
        ),
    ]
