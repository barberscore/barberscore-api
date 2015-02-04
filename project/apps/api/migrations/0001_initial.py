# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields
import timezone_field.fields
import autoslug.fields
import apps.api.models
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, max_length=32, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the award.  Must be unique.', unique=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('description', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, max_length=32, serialize=False, editable=False, primary_key=True)),
                ('kind', models.IntegerField(default=1, choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate')])),
                ('year', models.IntegerField(default=2015, choices=[(2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)])),
                ('slug', autoslug.fields.AutoSlugField(null=True, editable=False, blank=True, unique=True)),
                ('panel', models.IntegerField(default=5, help_text=b'\n            Size of the judging panel (typically\n            three or five.)')),
                ('scoresheet', models.FileField(null=True, upload_to=b'', blank=True)),
                ('csv_quarters', models.FileField(null=True, upload_to=b'', blank=True)),
                ('csv_semis', models.FileField(null=True, upload_to=b'', blank=True)),
                ('csv_finals', models.FileField(null=True, upload_to=b'', blank=True)),
            ],
            options={
                'ordering': ['convention__district', 'kind', 'convention__year'],
            },
        ),
        migrations.CreateModel(
            name='Convention',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, max_length=32, serialize=False, editable=False, primary_key=True)),
                ('kind', models.IntegerField(default=1, choices=[(1, b'Summer'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring')])),
                ('year', models.IntegerField(default=2015, choices=[(2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)])),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('dates', models.CharField(max_length=200, null=True, blank=True)),
                ('location', models.CharField(max_length=200, null=True, blank=True)),
                ('timezone', timezone_field.fields.TimeZoneField(default=b'US/Pacific')),
            ],
            options={
                'ordering': ['district', 'kind', 'year'],
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, max_length=32, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the resource.  Must be unique.  If there are singer name conflicts, please add middle initial, nickname, or other identifying information.', unique=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('location', models.CharField(help_text=b'\n            The geographical location of the resource.', max_length=200, blank=True)),
                ('website', models.URLField(help_text=b'\n            The website URL of the resource.', blank=True)),
                ('facebook', models.URLField(help_text=b'\n            The facebook URL of the resource.', blank=True)),
                ('twitter', models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the resource.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')])),
                ('email', models.EmailField(help_text=b'\n            The contact email of the resource.', max_length=254, null=True, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.  Include country code.', max_length=128, null=True, verbose_name=b'Phone Number', blank=True)),
                ('picture', models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True)),
                ('description', models.TextField(help_text=b'\n            A description/bio of the resource.  Max 1000 characters.', max_length=1000, blank=True)),
                ('notes', models.TextField(help_text=b'\n            Notes (for internal use only).', null=True, blank=True)),
                ('long_name', models.CharField(max_length=200, null=True, blank=True)),
                ('kind', models.IntegerField(default=0, choices=[(0, b'BHS'), (1, b'District'), (2, b'Affiliate')])),
            ],
            options={
                'ordering': ['kind', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, max_length=32, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the resource.  Must be unique.  If there are singer name conflicts, please add middle initial, nickname, or other identifying information.', unique=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('location', models.CharField(help_text=b'\n            The geographical location of the resource.', max_length=200, blank=True)),
                ('website', models.URLField(help_text=b'\n            The website URL of the resource.', blank=True)),
                ('facebook', models.URLField(help_text=b'\n            The facebook URL of the resource.', blank=True)),
                ('twitter', models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the resource.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')])),
                ('email', models.EmailField(help_text=b'\n            The contact email of the resource.', max_length=254, null=True, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.  Include country code.', max_length=128, null=True, verbose_name=b'Phone Number', blank=True)),
                ('picture', models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True)),
                ('description', models.TextField(help_text=b'\n            A description/bio of the resource.  Max 1000 characters.', max_length=1000, blank=True)),
                ('notes', models.TextField(help_text=b'\n            Notes (for internal use only).', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupAward',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, max_length=32, serialize=False, editable=False, primary_key=True)),
                ('award', models.ForeignKey(to='api.Award')),
                ('contest', models.ForeignKey(to='api.Contest')),
            ],
        ),
        migrations.CreateModel(
            name='GroupFinish',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, max_length=32, serialize=False, editable=False, primary_key=True)),
                ('place', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49)])),
                ('prelim', models.FloatField(null=True, blank=True)),
                ('seed', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49)])),
                ('score', models.FloatField(null=True, blank=True)),
                ('contest', models.ForeignKey(blank=True, to='api.Contest', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, max_length=32, serialize=False, editable=False, primary_key=True)),
                ('part', models.IntegerField(blank=True, null=True, choices=[(1, b'Lead'), (2, b'Tenor'), (3, b'Baritone'), (4, b'Bass')])),
                ('contest', models.ForeignKey(to='api.Contest')),
            ],
            options={
                'ordering': ['group', 'part', 'singer', 'contest'],
            },
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, max_length=32, serialize=False, editable=False, primary_key=True)),
                ('round', models.IntegerField(default=1, choices=[(1, b'Finals'), (2, b'Semi-Finals'), (3, b'Quarter-Finals')])),
                ('queue', models.IntegerField(null=True, blank=True)),
                ('stagetime', models.DateTimeField(help_text=b'\n            The title of the first song of the performance.', null=True, blank=True)),
                ('place', models.IntegerField(null=True, blank=True)),
                ('song1', models.CharField(help_text=b'\n            The title of the first song of the performance.', max_length=200, blank=True)),
                ('mus1', models.IntegerField(help_text=b'\n            The raw music score of the first song.', null=True, blank=True)),
                ('prs1', models.IntegerField(help_text=b'\n            The raw presentation score of the first song.', null=True, blank=True)),
                ('sng1', models.IntegerField(help_text=b'\n            The raw singing score of the first song.', null=True, blank=True)),
                ('song2', models.CharField(help_text=b'\n            The title of the second song of the performance.', max_length=200, blank=True)),
                ('mus2', models.IntegerField(help_text=b'\n            The raw music score of the second song.', null=True, blank=True)),
                ('prs2', models.IntegerField(help_text=b'\n            The raw presentation score of the second song.', null=True, blank=True)),
                ('sng2', models.IntegerField(help_text=b'\n            The raw singing score of the second song.', null=True, blank=True)),
                ('contest', models.ForeignKey(related_name='performances', to='api.Contest')),
            ],
            options={
                'ordering': ['-contest', 'round', 'group'],
            },
        ),
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, max_length=32, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the resource.  Must be unique.  If there are singer name conflicts, please add middle initial, nickname, or other identifying information.', unique=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('location', models.CharField(help_text=b'\n            The geographical location of the resource.', max_length=200, blank=True)),
                ('website', models.URLField(help_text=b'\n            The website URL of the resource.', blank=True)),
                ('facebook', models.URLField(help_text=b'\n            The facebook URL of the resource.', blank=True)),
                ('twitter', models.CharField(blank=True, help_text=b'\n            The twitter handle (in form @twitter_handle) of the resource.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'@([A-Za-z0-9_]+)', message=b'\n                    Must be a single Twitter handle\n                    in the form `@twitter_handle`.\n                ')])),
                ('email', models.EmailField(help_text=b'\n            The contact email of the resource.', max_length=254, null=True, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.  Include country code.', max_length=128, null=True, verbose_name=b'Phone Number', blank=True)),
                ('picture', models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True)),
                ('description', models.TextField(help_text=b'\n            A description/bio of the resource.  Max 1000 characters.', max_length=1000, blank=True)),
                ('notes', models.TextField(help_text=b'\n            Notes (for internal use only).', null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Chorus',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='api.Group')),
                ('director', models.CharField(help_text=b'\n            The name of the director(s) of the chorus.', max_length=200, blank=True)),
                ('chapter_name', models.CharField(help_text=b'\n            The name of the director(s) of the chorus.', max_length=200, blank=True)),
                ('chapter_code', models.CharField(help_text=b'\n            The code of the director(s) of the chorus.', max_length=200, blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'choruses',
            },
            bases=('api.group',),
        ),
        migrations.CreateModel(
            name='Quartet',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='api.Group')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('api.group',),
        ),
        migrations.AddField(
            model_name='performance',
            name='group',
            field=models.ForeignKey(related_name='performances', to='api.Group'),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='group',
            field=models.ForeignKey(to='api.Group'),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='singer',
            field=models.ForeignKey(to='api.Singer'),
        ),
        migrations.AddField(
            model_name='groupfinish',
            name='group',
            field=models.ForeignKey(blank=True, to='api.Group', null=True),
        ),
        migrations.AddField(
            model_name='groupaward',
            name='group',
            field=models.ForeignKey(to='api.Group'),
        ),
        migrations.AddField(
            model_name='group',
            name='awards',
            field=models.ManyToManyField(related_name='groups', through='api.GroupAward', to='api.Award'),
        ),
        migrations.AddField(
            model_name='group',
            name='district',
            field=models.ForeignKey(related_name='groups', blank=True, to='api.District', help_text=b'\n            This is the district the group is officially representing in the contest.', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='groups', through='api.GroupMember', to='api.Singer'),
        ),
        migrations.AddField(
            model_name='convention',
            name='district',
            field=models.ForeignKey(to='api.District'),
        ),
        migrations.AddField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(blank=True, to='api.Convention', null=True),
        ),
        migrations.AddField(
            model_name='contest',
            name='district',
            field=models.ForeignKey(to='api.District'),
        ),
    ]
