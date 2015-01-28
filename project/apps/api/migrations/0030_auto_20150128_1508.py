# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timezone_field.fields
import django_pg.models.fields.uuid
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20150127_1142'),
    ]

    operations = [
        migrations.CreateModel(
            name='Convention',
            fields=[
                ('id', django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True)),
                ('year', models.IntegerField(default=2015, max_length=4, choices=[(2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)])),
                ('level', models.IntegerField(default=1, choices=[(1, b'International')])),
                ('kind', models.IntegerField(default=1, choices=[(1, b'Summer')])),
                ('dates', models.CharField(max_length=200, null=True, blank=True)),
                ('location', models.CharField(max_length=200, null=True, blank=True)),
                ('timezone', timezone_field.fields.TimeZoneField(default=b'US/Pacific')),
            ],
            options={
                'ordering': ['-year', 'level', 'kind'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='chorusperformance',
            name='round',
            field=models.IntegerField(default=1, choices=[(1, b'Finals'), (2, b'Semi-Finals'), (3, b'Quarter-Finals')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contest',
            name='level',
            field=models.IntegerField(default=1, choices=[(1, b'International')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quartetperformance',
            name='round',
            field=models.IntegerField(default=3, choices=[(1, b'Finals'), (2, b'Semi-Finals'), (3, b'Quarter-Finals')]),
            preserve_default=True,
        ),
    ]
