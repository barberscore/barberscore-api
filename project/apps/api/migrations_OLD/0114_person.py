# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import apps.api.models
import django.core.validators
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0113_auto_20150630_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the resource.  Must be unique.  If there are singer name conflicts, please add middle initial, nickname, or other identifying information.', unique=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True)),
                ('location', models.CharField(help_text=b'\n            The geographical location of the resource.', max_length=200, blank=True)),
                ('website', models.URLField(help_text=b'\n            The website URL of the resource.', blank=True)),
                ('facebook', models.URLField(help_text=b'\n            The facebook URL of the resource.', blank=True)),
                ('twitter', models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the resource.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')])),
                ('email', models.EmailField(help_text=b'\n            The contact email of the resource.', max_length=254, null=True, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.  Include country code.', max_length=128, null=True, blank=True)),
                ('picture', models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True)),
                ('description', models.TextField(help_text=b'\n            A description/bio of the resource.  Max 1000 characters.', max_length=1000, blank=True)),
                ('notes', models.TextField(help_text=b'\n            Notes (for internal use only).', null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
