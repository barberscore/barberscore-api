# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.api.models
import model_utils.fields
import apps.api.validators
import autoslug.fields
import mptt.fields
import django.utils.timezone
import phonenumber_field.modelfields
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0062_auto_20151024_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the resource.', max_length=200, unique=True, error_messages={b'unique': b'The name must be unique.  Add middle initials, suffixes, years, or other identifiers to make the name unique.'}, validators=[apps.api.validators.validate_trimmed])),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('start', models.DateField(help_text=b'\n            The founding/birth date of the resource.', null=True, blank=True)),
                ('end', models.DateField(help_text=b'\n            The retirement/deceased date of the resource.', null=True, blank=True)),
                ('location', models.CharField(help_text=b'\n            The geographical location of the resource.', max_length=200, blank=True)),
                ('website', models.URLField(help_text=b'\n            The website URL of the resource.', blank=True)),
                ('facebook', models.URLField(help_text=b'\n            The facebook URL of the resource.', blank=True)),
                ('twitter', models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the resource.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')])),
                ('email', models.EmailField(help_text=b'\n            The contact email of the resource.', max_length=254, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.  Include country code.', max_length=128, null=True, blank=True)),
                ('picture', models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True)),
                ('description', models.TextField(help_text=b'\n            A description/bio of the resource.  Max 1000 characters.', max_length=1000, blank=True)),
                ('notes', models.TextField(help_text=b'\n            Notes (for internal use only).', blank=True)),
                ('is_active', models.BooleanField(default=True, help_text=b'\n            A boolean for active/living resources.')),
                ('long_name', models.CharField(help_text=b'\n            A long-form name for the resource.', max_length=200, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='api.Organization', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
