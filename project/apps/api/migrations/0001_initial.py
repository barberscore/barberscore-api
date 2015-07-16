# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import phonenumber_field.modelfields
import model_utils.fields
import autoslug.fields
import django.db.models.deletion
import django.utils.timezone
import apps.api.models
import timezone_field.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('status', model_utils.fields.StatusField(default=b'Upcoming', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'Upcoming', b'Upcoming'), (b'Current', b'Current'), (b'Pending', b'Pending'), (b'Complete', b'Complete')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('level', models.IntegerField(default=1, choices=[(1, b'International')])),
                ('kind', models.IntegerField(default=1, choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate')])),
                ('year', models.IntegerField(default=2015, choices=[(2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981), (1980, 1980), (1979, 1979), (1978, 1978), (1977, 1977), (1976, 1976), (1975, 1975), (1974, 1974), (1973, 1973), (1972, 1972), (1971, 1971), (1970, 1970), (1969, 1969), (1968, 1968), (1967, 1967), (1966, 1966), (1965, 1965), (1964, 1964), (1963, 1963), (1962, 1962), (1961, 1961), (1960, 1960), (1959, 1959), (1958, 1958), (1957, 1957), (1956, 1956), (1955, 1955), (1954, 1954), (1953, 1953), (1952, 1952), (1951, 1951), (1950, 1950), (1949, 1949), (1948, 1948), (1947, 1947), (1946, 1946), (1945, 1945), (1944, 1944), (1943, 1943), (1942, 1942), (1941, 1941), (1940, 1940), (1939, 1939)])),
                ('panel', models.IntegerField(default=5, help_text=b'\n            Size of the judging panel (typically\n            three or five.)')),
                ('scoresheet_pdf', models.FileField(null=True, upload_to=apps.api.models.generate_image_filename, blank=True)),
                ('scoresheet_csv', models.FileField(null=True, upload_to=apps.api.models.generate_image_filename, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_complete', models.BooleanField(default=False)),
                ('is_place', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('level', '-year', 'kind'),
            },
        ),
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('start', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='end', blank=True)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('picture', models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True)),
                ('seed', models.IntegerField(null=True, blank=True)),
                ('prelim', models.FloatField(null=True, blank=True)),
                ('points', models.IntegerField(null=True, blank=True)),
                ('score', models.FloatField(null=True, blank=True)),
                ('place', models.IntegerField(null=True, blank=True)),
                ('stagetime', models.DateTimeField(null=True, blank=True)),
                ('draw', models.IntegerField(null=True, blank=True)),
                ('men', models.IntegerField(null=True, blank=True)),
                ('quarters_points', models.IntegerField(null=True, blank=True)),
                ('semis_points', models.IntegerField(null=True, blank=True)),
                ('finals_points', models.IntegerField(null=True, blank=True)),
                ('quarters_score', models.FloatField(null=True, blank=True)),
                ('semis_score', models.FloatField(null=True, blank=True)),
                ('finals_score', models.FloatField(null=True, blank=True)),
                ('quarters_place', models.IntegerField(null=True, blank=True)),
                ('semis_place', models.IntegerField(null=True, blank=True)),
                ('finals_place', models.IntegerField(null=True, blank=True)),
                ('contest', models.ForeignKey(related_name='contestants', to='api.Contest')),
            ],
            options={
                'ordering': ('-contest__year', 'place', '-score'),
            },
        ),
        migrations.CreateModel(
            name='Convention',
            fields=[
                ('start', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='end', blank=True)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'\n            The name of the convention.', unique=True, max_length=200)),
                ('kind', models.IntegerField(blank=True, null=True, choices=[(1, b'International'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (5, b'Pacific')])),
                ('year', models.IntegerField(default=2015, null=True, blank=True, choices=[(2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981), (1980, 1980), (1979, 1979), (1978, 1978), (1977, 1977), (1976, 1976), (1975, 1975), (1974, 1974), (1973, 1973), (1972, 1972), (1971, 1971), (1970, 1970), (1969, 1969), (1968, 1968), (1967, 1967), (1966, 1966), (1965, 1965), (1964, 1964), (1963, 1963), (1962, 1962), (1961, 1961), (1960, 1960), (1959, 1959), (1958, 1958), (1957, 1957), (1956, 1956), (1955, 1955), (1954, 1954), (1953, 1953), (1952, 1952), (1951, 1951), (1950, 1950), (1949, 1949), (1948, 1948), (1947, 1947), (1946, 1946), (1945, 1945), (1944, 1944), (1943, 1943), (1942, 1942), (1941, 1941), (1940, 1940), (1939, 1939)])),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True)),
                ('dates', models.CharField(max_length=200, null=True, blank=True)),
                ('location', models.CharField(max_length=200, null=True, blank=True)),
                ('timezone', timezone_field.fields.TimeZoneField(default=b'US/Pacific')),
                ('is_active', models.BooleanField(default=False)),
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
                ('kind', models.IntegerField(default=1, choices=[(1, b'Quartet'), (2, b'Chorus')])),
                ('chapter_name', models.CharField(help_text=b'\n            The name of the director(s) of the chorus.', max_length=200, null=True, blank=True)),
                ('chapter_code', models.CharField(help_text=b'\n            The code of the director(s) of the chorus.', max_length=200, blank=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('round', models.IntegerField(choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')])),
                ('order', models.IntegerField(choices=[(1, b'1'), (2, b'2')])),
                ('mus_points', models.IntegerField(null=True, blank=True)),
                ('prs_points', models.IntegerField(null=True, blank=True)),
                ('sng_points', models.IntegerField(null=True, blank=True)),
                ('total_points', models.IntegerField(null=True, blank=True)),
                ('mus_score', models.FloatField(null=True, blank=True)),
                ('prs_score', models.FloatField(null=True, blank=True)),
                ('sng_score', models.FloatField(null=True, blank=True)),
                ('total_score', models.FloatField(null=True, blank=True)),
                ('penalty', models.TextField(null=True, blank=True)),
                ('chart', models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Chart', null=True)),
                ('contestant', models.ForeignKey(related_name='performances', to='api.Contestant')),
            ],
            options={
                'ordering': ['contestant', 'round', 'order'],
            },
        ),
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
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('part', models.IntegerField(blank=True, null=True, choices=[(1, b'Tenor'), (2, b'Lead'), (3, b'Baritone'), (4, b'Bass')])),
                ('contestant', models.ForeignKey(related_name='singers', to='api.Contestant')),
                ('person', models.ForeignKey(related_name='quartets', to='api.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('is_medley', models.BooleanField(default=False)),
                ('is_parody', models.BooleanField(default=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='director',
            name='person',
            field=models.ForeignKey(related_name='choruses', to='api.Person'),
        ),
        migrations.AddField(
            model_name='convention',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='district',
            field=models.ForeignKey(related_name='contestants', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='group',
            field=models.ForeignKey(related_name='contestants', to='api.Group'),
        ),
        migrations.AddField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(related_name='contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Convention', null=True),
        ),
        migrations.AddField(
            model_name='contest',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', null=True),
        ),
        migrations.AddField(
            model_name='chart',
            name='arranger',
            field=models.ForeignKey(related_name='charts', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='chart',
            name='song',
            field=models.ForeignKey(related_name='charts', to='api.Song'),
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
    ]
