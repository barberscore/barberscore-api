# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import phonenumber_field.modelfields
import uuid
import django_pg.models.fields.uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chorus',
            fields=[
                ('id', django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the chorus.', max_length=200)),
                ('slug', models.SlugField(null=True, max_length=200, blank=True, help_text=b'\n            The slug, generated in a signal from the name field.', unique=True)),
                ('location', models.CharField(help_text=b'\n            The geographical location of the contestant.', max_length=200, blank=True)),
                ('website', models.URLField(help_text=b'\n            The website URL of the contestant.', blank=True)),
                ('facebook', models.URLField(help_text=b'\n            The facebook URL of the contestant.', blank=True)),
                ('twitter', models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the contestant.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')])),
                ('email', models.EmailField(help_text=b'\n            The contact email of the contestant.', max_length=75, blank=True)),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(null=True, max_length=128, blank=True, help_text=b'\n            The Full Name of the Singer.', unique=True, verbose_name=b'mobile number')),
                ('director', models.CharField(help_text=b'\n            The name of the director(s) of the chorus.', max_length=200, blank=True)),
                ('district', models.IntegerField(help_text=b'\n            The district the\n            contestant is representing.', null=True, blank=True)),
                ('picture', models.ImageField(help_text=b"\n            The 'official' picture of the contestant.", null=True, upload_to=b'', blank=True)),
                ('blurb', models.TextField(help_text=b'\n            A blurb describing the contestant.  Max 1000 characters.', max_length=1000, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
    ]
