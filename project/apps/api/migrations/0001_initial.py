# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timezone_field.fields
import phonenumber_field.modelfields
import django_pg.models.fields.uuid
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True)),
                ('full_name', models.CharField(help_text=b'\n            The Full Name of the Singer.', max_length=100, null=True, verbose_name=b'Full Name', blank=True)),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(null=True, max_length=128, blank=True, help_text=b'\n            The Full Name of the Singer.', unique=True, verbose_name=b'mobile number')),
                ('email', models.EmailField(help_text=b'\n            The Email Address of the User.', max_length=75, null=True, verbose_name=b'Email Address', blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('timezone', timezone_field.fields.TimeZoneField(default=b'US/Pacific')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
