# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import django.core.validators
import django_pg.models.fields.uuid
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_quartetperformance'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChorusPerformance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round', models.IntegerField(default=1, choices=[(1, b'Finals')])),
                ('chorus', models.ForeignKey(to='api.Chorus')),
                ('contest', models.ForeignKey(to='api.Contest')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Collegiate',
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
            name='CollegiateMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('part', models.IntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Lead'), (2, b'Tenor'), (3, b'Baritone'), (4, b'Bass')])),
                ('collegiate', models.ForeignKey(to='api.Collegiate')),
                ('contest', models.ForeignKey(default=None, blank=True, to='api.Contest', null=True)),
                ('singer', models.ForeignKey(to='api.Singer')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollegiatePerformance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round', models.IntegerField(default=1, choices=[(1, b'Finals')])),
                ('collegiate', models.ForeignKey(to='api.Collegiate')),
                ('contest', models.ForeignKey(to='api.Contest')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='collegiate',
            name='members',
            field=models.ManyToManyField(to='api.Singer', null=True, through='api.CollegiateMembership', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contest',
            name='kind',
            field=models.IntegerField(default=1, choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate')]),
            preserve_default=True,
        ),
    ]
