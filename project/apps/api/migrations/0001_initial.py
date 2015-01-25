# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import timezone_field.fields
import autoslug.fields
import django_pg.models.fields.uuid
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the district.', max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Chorus',
            fields=[
                ('id', django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the chorus.', max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('location', models.CharField(help_text=b'\n            The geographical location of the contestant.', max_length=200, blank=True)),
                ('website', models.URLField(help_text=b'\n            The website URL of the contestant.', blank=True)),
                ('facebook', models.URLField(help_text=b'\n            The facebook URL of the contestant.', blank=True)),
                ('twitter', models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the contestant.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')])),
                ('email', models.EmailField(help_text=b'\n            The contact email of the contestant.', max_length=75, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The Full Name of the Singer.', max_length=128, null=True, verbose_name=b'mobile number', blank=True)),
                ('director', models.CharField(help_text=b'\n            The name of the director(s) of the chorus.', max_length=200, blank=True)),
                ('picture', models.ImageField(help_text=b"\n            The 'official' picture of the contestant.", null=True, upload_to=b'', blank=True)),
                ('blurb', models.TextField(help_text=b'\n            A blurb describing the contestant.  Max 1000 characters.', max_length=1000, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'choruses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the district.', max_length=200)),
                ('abbreviation', models.CharField(max_length=20, null=True, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('location', models.CharField(help_text=b'\n            The geographical location of the district.', max_length=200, blank=True)),
                ('website', models.URLField(help_text=b'\n            The website URL of the district.', blank=True)),
                ('facebook', models.URLField(help_text=b'\n            The facebook URL of the district.', blank=True)),
                ('twitter', models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the district.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')])),
                ('email', models.EmailField(help_text=b'\n            The contact email of the district.', max_length=75, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            District phone number.', max_length=128, null=True, verbose_name=b'mobile number', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quartet',
            fields=[
                ('id', django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the quartet.', max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('location', models.CharField(help_text=b'\n            The geographical location of the quartet.', max_length=200, blank=True)),
                ('website', models.URLField(help_text=b'\n            The website URL of the quartet.', blank=True)),
                ('facebook', models.URLField(help_text=b'\n            The facebook URL of the quartet.', blank=True)),
                ('twitter', models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the quartet.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')])),
                ('email', models.EmailField(help_text=b'\n            The contact email of the quartet.', max_length=75, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The contact number of the quartet.', max_length=128, null=True, verbose_name=b'mobile number', blank=True)),
                ('picture', models.ImageField(help_text=b"\n            The 'official' picture of the contestant.", null=True, upload_to=b'', blank=True)),
                ('blurb', models.TextField(help_text=b'\n            A blurb describing the contestant.  Max 1000 characters.', max_length=1000, blank=True)),
                ('district', models.ForeignKey(blank=True, to='api.District', help_text=b'\n            The district the quartet is representing.', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuartetMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('part', models.IntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Lead'), (2, b'Tenor'), (3, b'Baritone'), (4, b'Bass')])),
                ('quartet', models.ForeignKey(to='api.Quartet')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', django_pg.models.fields.uuid.UUIDField(default=uuid.uuid4, unique=True, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The Full Name of the Singer.', max_length=100, verbose_name=b'Full Name')),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone of the Singer.', max_length=128, null=True, verbose_name=b'mobile number', blank=True)),
                ('email', models.EmailField(help_text=b'\n            The Email Address of the singer.', max_length=75, null=True, verbose_name=b'Email Address', blank=True)),
                ('bio', models.TextField(help_text=b'\n            A quick biography of the singer.', null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('timezone', timezone_field.fields.TimeZoneField(default=b'US/Pacific')),
                ('chapter', models.ForeignKey(blank=True, to='api.Chapter', help_text=b'\n            The chapter of the singer.', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='quartetmembership',
            name='singer',
            field=models.ForeignKey(to='api.Singer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartet',
            name='members',
            field=models.ManyToManyField(to='api.Singer', null=True, through='api.QuartetMembership', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chorus',
            name='district',
            field=models.ForeignKey(blank=True, to='api.District', help_text=b'\n            The district the\n            contestant is representing.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chapter',
            name='district',
            field=models.ForeignKey(to='api.District'),
            preserve_default=True,
        ),
    ]
