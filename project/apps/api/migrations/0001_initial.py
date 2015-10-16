# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.api.models
import phonenumber_field.modelfields
import timezone_field.fields
import apps.api.validators
import autoslug.fields
import django.db.models.deletion
import django.utils.timezone
import django.core.validators
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('email', models.EmailField(help_text=b'Your email address will be your username.', unique=True, max_length=254)),
                ('name', models.CharField(help_text=b'Your full name.', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Arranger',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('part', models.IntegerField(default=1, choices=[(1, b'Arranger'), (2, b'Co-Arranger')])),
            ],
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('kind', models.IntegerField(choices=[(1, b'First Place Gold Medalist'), (2, b'Second Place Silver Medalist'), (3, b'Third Place Bronze Medalist'), (4, b'Fourth Place Bronze Medalist'), (5, b'Fifth Place Bronze Medalist')])),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('bhs_id', models.IntegerField(null=True, blank=True)),
                ('bhs_published', models.DateField(null=True, blank=True)),
                ('bhs_songname', models.CharField(max_length=200, blank=True)),
                ('bhs_arranger', models.CharField(max_length=200, blank=True)),
                ('bhs_fee', models.FloatField(null=True, blank=True)),
                ('bhs_difficulty', models.IntegerField(blank=True, null=True, choices=[(1, b'Very Easy'), (2, b'Easy'), (3, b'Medium'), (4, b'Hard'), (5, b'Very Hard')])),
                ('bhs_tempo', models.IntegerField(blank=True, null=True, choices=[(1, b'Ballad'), (2, b'Uptune'), (3, b'Mixed')])),
                ('bhs_medley', models.BooleanField(default=False)),
                ('is_parody', models.BooleanField(default=False)),
                ('is_medley', models.BooleanField(default=False)),
                ('song_match', models.CharField(max_length=200, blank=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('person_match', models.CharField(max_length=200, blank=True)),
                ('fuzzy', models.TextField(blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('name', models.CharField(help_text=b'\n            The name of the contest (determined programmatically.)', unique=True, max_length=200)),
                ('level', models.IntegerField(default=1, help_text=b'\n            The level of the contest (currently only International is supported.)', choices=[(1, b'International')])),
                ('kind', models.IntegerField(default=1, help_text=b'\n            The kind of the contest (quartet, chorus, senior, collegiate.)', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate')])),
                ('year', models.IntegerField(default=2015, validators=[django.core.validators.MaxValueValidator(2016, message=b'Year must be between 1939 and 2016'), django.core.validators.MinValueValidator(1938, message=b'Year must be between 1939 and 2016')])),
                ('panel', models.IntegerField(default=5, help_text=b'\n            Size of the judging panel (typically three or five.)')),
                ('scoresheet_pdf', models.FileField(help_text=b'\n            PDF of the OSS.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True)),
                ('scoresheet_csv', models.FileField(help_text=b'\n            The parsed scoresheet (used for legacy imports).', null=True, upload_to=apps.api.models.generate_image_filename, blank=True)),
                ('is_active', models.BooleanField(default=False, help_text=b'\n            A global boolean that controls if the resource is accessible via the API')),
                ('status', models.IntegerField(default=0, choices=[(0, b'New'), (1, b'Upcoming'), (2, b'Current'), (3, b'Reviewing'), (4, b'Complete')])),
            ],
            options={
                'ordering': ('level', '-year', 'kind'),
            },
        ),
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('picture', models.ImageField(help_text=b'\n            The performance picture (as opposed to the "official" photo).', null=True, upload_to=apps.api.models.generate_image_filename, blank=True)),
                ('seed', models.IntegerField(help_text=b'\n            The incoming rank based on prelim score.', null=True, blank=True)),
                ('prelim', models.FloatField(help_text=b'\n            The incoming prelim score.', null=True, blank=True)),
                ('points', models.IntegerField(help_text=b'\n            Total raw points for this contestant (cumuative).', null=True, blank=True)),
                ('score', models.FloatField(help_text=b'\n            The percentile of the total points (cumulative , all sessions).', null=True, blank=True)),
                ('place', models.IntegerField(help_text=b'\n            The final placement/rank of the contestant.', null=True, blank=True)),
                ('men', models.IntegerField(help_text=b'\n            The number of men on stage (only for chourses).', null=True, blank=True)),
                ('quarters_points', models.IntegerField(help_text=b'\n            The total points for the quarterfinal session.', null=True, blank=True)),
                ('semis_points', models.IntegerField(help_text=b'\n            The total points for the semifinal session.', null=True, blank=True)),
                ('finals_points', models.IntegerField(help_text=b'\n            The total points for the final session.', null=True, blank=True)),
                ('quarters_score', models.FloatField(help_text=b'\n            The percential score for the quarterfinal session.', null=True, blank=True)),
                ('semis_score', models.FloatField(help_text=b'\n            The percential score for the semifinal session.', null=True, blank=True)),
                ('finals_score', models.FloatField(help_text=b'\n            The percential score for the final session.', null=True, blank=True)),
                ('quarters_place', models.IntegerField(help_text=b'\n            The place for the quarterfinal session.  This is for the quarters only and is NOT cumulative.', null=True, blank=True)),
                ('semis_place', models.IntegerField(help_text=b'\n            The place for the semifinal session.  This is for the semis only and is NOT cumulative.', null=True, blank=True)),
                ('finals_place', models.IntegerField(help_text=b'\n            The place for the fainal session.  This is for the finals only and is NOT cumulative.', null=True, blank=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b'New')])),
                ('contest', models.ForeignKey(related_name='contestants', to='api.Contest')),
            ],
            options={
                'ordering': ('-contest__year', 'place', '-score'),
            },
        ),
        migrations.CreateModel(
            name='Convention',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the convention (determined programmatically.)', unique=True, max_length=200)),
                ('kind', models.IntegerField(help_text=b'\n            The kind of convention.', choices=[(1, b'International'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (5, b'Pacific')])),
                ('year', models.IntegerField(default=2015, validators=[django.core.validators.MaxValueValidator(2016, message=b'Year must be between 1939 and 2016'), django.core.validators.MinValueValidator(1938, message=b'Year must be between 1939 and 2016')])),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('dates', models.CharField(help_text=b'\n            The convention dates (will be replaced by start/end).', max_length=200, blank=True)),
                ('location', models.CharField(help_text=b'\n            The location of the convention.', max_length=200, blank=True)),
                ('timezone', timezone_field.fields.TimeZoneField(default=b'US/Pacific', help_text=b'\n            The local timezone of the convention.')),
                ('is_active', models.BooleanField(default=False, help_text=b'\n            A global boolean that controls if the resource is accessible via the API')),
            ],
            options={
                'ordering': ['district', '-year'],
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('part', models.IntegerField(default=1, choices=[(1, b'Director'), (2, b'Co-Director')])),
                ('contestant', models.ForeignKey(related_name='directors', to='api.Contestant')),
            ],
        ),
        migrations.CreateModel(
            name='District',
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
                ('kind', models.IntegerField(default=0, help_text=b'\n            The kind of District.  Choices are BHS (International), District, and Affiliate.', choices=[(0, b'BHS'), (1, b'District'), (2, b'Affiliate')])),
                ('long_name', models.CharField(help_text=b'\n            A long-form name for the resource.', max_length=200, blank=True)),
            ],
            options={
                'ordering': ['kind', 'name'],
            },
        ),
        migrations.CreateModel(
            name='DuplicateGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DuplicatePerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DuplicateSong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('start', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='end', blank=True)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the event (determined programmatically.)', unique=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('draw', models.IntegerField(help_text=b'\n            The OA (Order of Appearance) in the contest schedule.  Specific to each session.', null=True, blank=True)),
                ('kind', models.IntegerField(help_text=b'\n            The kind of event.', choices=[(b'Session', [(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')]), (b'Other', [(4, b'Other')])])),
                ('location', models.CharField(help_text=b'\n            The location of the event.', max_length=200, blank=True)),
                ('is_active', models.BooleanField(default=False, help_text=b'\n            A global boolean that controls if the resource is accessible via the API')),
                ('contest', models.ForeignKey(related_name='events', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Contest', help_text=b'\n            The contest associated with this event.', null=True)),
                ('contestant', models.ForeignKey(related_name='events', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Contestant', help_text=b'\n            The contestant associated with this event.', null=True)),
                ('convention', models.ForeignKey(related_name='events', to='api.Convention', help_text=b'\n            The convention at which this event occurs.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
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
                ('kind', models.IntegerField(default=1, help_text=b'\n            The kind of group; choices are Quartet or Chorus.', choices=[(1, b'Quartet'), (2, b'Chorus')])),
                ('chapter_name', models.CharField(help_text=b'\n            The chapter name (only for choruses).', max_length=200, blank=True)),
                ('chapter_code', models.CharField(help_text=b'\n            The chapter code (only for choruses).', max_length=200, blank=True)),
                ('fuzzy', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b'New')])),
                ('part', models.IntegerField(choices=[(1, b'Music'), (2, b'Presentation'), (3, b'Singing'), (4, b'Administrator')])),
                ('num', models.IntegerField()),
                ('contest', models.ForeignKey(related_name='judges', to='api.Contest')),
            ],
            options={
                'ordering': ('contest', 'part', 'num'),
            },
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b'New')])),
                ('session', models.IntegerField(choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')])),
                ('order', models.IntegerField(choices=[(1, b'First'), (2, b'Second')])),
                ('is_parody', models.BooleanField(default=False)),
                ('mus_points', models.IntegerField(help_text=b'\n            The total music points for this performance.', null=True, blank=True)),
                ('prs_points', models.IntegerField(help_text=b'\n            The total presentation points for this performance.', null=True, blank=True)),
                ('sng_points', models.IntegerField(help_text=b'\n            The total singing points for this performance.', null=True, blank=True)),
                ('total_points', models.IntegerField(help_text=b'\n            The total points for this performance.', null=True, blank=True)),
                ('mus_score', models.FloatField(help_text=b'\n            The percentile music score for this performance.', null=True, blank=True)),
                ('prs_score', models.FloatField(help_text=b'\n            The percentile presentation score for this performance.', null=True, blank=True)),
                ('sng_score', models.FloatField(help_text=b'\n            The percentile singing score for this performance.', null=True, blank=True)),
                ('total_score', models.FloatField(help_text=b'\n            The total percentile score for this performance.', null=True, blank=True)),
                ('penalty', models.TextField(help_text=b'\n            Free form for penalties (notes).', blank=True)),
                ('catalog', models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Catalog', null=True)),
                ('contestant', models.ForeignKey(related_name='performances', to='api.Contestant')),
            ],
            options={
                'ordering': ['contestant', 'session', 'order'],
            },
        ),
        migrations.CreateModel(
            name='Person',
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
                ('kind', models.IntegerField(default=1, help_text=b'\n            Most persons are individuals; however, they can be grouped into teams for the purpose of multi-arranger songs.', choices=[(1, b'Individual'), (2, b'Team')])),
                ('fuzzy', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('points', models.IntegerField(help_text=b'\n            The number of points awarded (0-100)', validators=[django.core.validators.MaxValueValidator(100, message=b'Points must be between 0 - 100'), django.core.validators.MinValueValidator(0, message=b'Points must be between 0 - 100')])),
                ('status', models.IntegerField(default=0, choices=[(0, b'New')])),
                ('category', models.IntegerField(choices=[(1, b'Music'), (2, b'Presentation'), (3, b'Singing'), (4, b'Admin')])),
                ('is_practice', models.BooleanField(default=False)),
                ('judge', models.ForeignKey(related_name='scores', to='api.Judge')),
                ('performance', models.ForeignKey(related_name='scores', to='api.Performance')),
            ],
        ),
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('part', models.IntegerField(choices=[(1, b'Tenor'), (2, b'Lead'), (3, b'Baritone'), (4, b'Bass')])),
                ('contestant', models.ForeignKey(related_name='singers', to='api.Contestant')),
                ('person', models.ForeignKey(related_name='quartets', to='api.Person')),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('fuzzy', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='performance',
            name='person',
            field=models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='song',
            field=models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='judge',
            name='person',
            field=models.ForeignKey(related_name='panels', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='duplicatesong',
            name='child',
            field=models.ForeignKey(related_name='children', to='api.Song'),
        ),
        migrations.AddField(
            model_name='duplicatesong',
            name='parent',
            field=models.ForeignKey(related_name='duplicates', to='api.Song'),
        ),
        migrations.AddField(
            model_name='duplicateperson',
            name='child',
            field=models.ForeignKey(related_name='children', to='api.Person'),
        ),
        migrations.AddField(
            model_name='duplicateperson',
            name='parent',
            field=models.ForeignKey(related_name='duplicates', to='api.Person'),
        ),
        migrations.AddField(
            model_name='duplicategroup',
            name='child',
            field=models.ForeignKey(related_name='children', to='api.Group'),
        ),
        migrations.AddField(
            model_name='duplicategroup',
            name='parent',
            field=models.ForeignKey(related_name='duplicates', to='api.Group'),
        ),
        migrations.AddField(
            model_name='director',
            name='person',
            field=models.ForeignKey(related_name='choruses', to='api.Person'),
        ),
        migrations.AddField(
            model_name='convention',
            name='district',
            field=models.ForeignKey(help_text=b"\n            The district for the convention.  If International, this is 'BHS'.", to='api.District'),
        ),
        migrations.AddField(
            model_name='contestant',
            name='district',
            field=models.ForeignKey(related_name='contestants', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', help_text=b'\n            The district this contestant is representing.', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='group',
            field=models.ForeignKey(related_name='contestants', to='api.Group'),
        ),
        migrations.AddField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(related_name='contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Convention', help_text=b'\n            The convention at which this contest occurred.', null=True),
        ),
        migrations.AddField(
            model_name='contest',
            name='district',
            field=models.ForeignKey(related_name='contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', null=True),
        ),
        migrations.AddField(
            model_name='catalog',
            name='person',
            field=models.ForeignKey(related_name='catalogs', blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='catalog',
            name='song',
            field=models.ForeignKey(related_name='catalogs', blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='award',
            name='contestant',
            field=models.ForeignKey(related_name='awards', to='api.Contestant'),
        ),
        migrations.AddField(
            model_name='arranger',
            name='performance',
            field=models.ForeignKey(to='api.Performance'),
        ),
        migrations.AddField(
            model_name='arranger',
            name='person',
            field=models.ForeignKey(to='api.Person'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='singer',
            unique_together=set([('contestant', 'person')]),
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('contestant', 'session', 'order')]),
        ),
        migrations.AlterUniqueTogether(
            name='judge',
            unique_together=set([('contest', 'part', 'num')]),
        ),
        migrations.AlterUniqueTogether(
            name='director',
            unique_together=set([('contestant', 'person')]),
        ),
        migrations.AlterUniqueTogether(
            name='convention',
            unique_together=set([('district', 'kind', 'year')]),
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('group', 'contest')]),
        ),
        migrations.AlterUniqueTogether(
            name='contest',
            unique_together=set([('level', 'kind', 'year', 'district')]),
        ),
        migrations.AlterUniqueTogether(
            name='catalog',
            unique_together=set([('person', 'song')]),
        ),
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set([('kind', 'contestant')]),
        ),
        migrations.AlterUniqueTogether(
            name='arranger',
            unique_together=set([('performance', 'person')]),
        ),
    ]
