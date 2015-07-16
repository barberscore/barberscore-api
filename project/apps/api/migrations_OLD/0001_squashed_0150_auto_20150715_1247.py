# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields
import timezone_field.fields
import autoslug.fields
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings
import apps.api.models
import django.core.validators
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    replaces = [(b'api', '0001_initial'), (b'api', '0002_performance_men'), (b'api', '0003_auto_20150205_0836'), (b'api', '0004_auto_20150208_0950'), (b'api', '0005_auto_20150208_1015'), (b'api', '0006_auto_20150213_0928'), (b'api', '0007_auto_20150306_1525'), (b'api', '0008_auto_20150308_0942'), (b'api', '0009_auto_20150421_1334'), (b'api', '0010_auto_20150421_1347'), (b'api', '0011_auto_20150421_1439'), (b'api', '0012_auto_20150421_1453'), (b'api', '0013_auto_20150426_1641'), (b'api', '0014_auto_20150429_0839'), (b'api', '0015_auto_20150429_2128'), (b'api', '0016_auto_20150501_1506'), (b'api', '0017_auto_20150504_0819'), (b'api', '0018_auto_20150504_0831'), (b'api', '0019_performance_apperance'), (b'api', '0020_auto_20150504_0926'), (b'api', '0021_auto_20150504_0939'), (b'api', '0022_auto_20150504_1018'), (b'api', '0023_auto_20150504_1120'), (b'api', '0024_auto_20150504_1405'), (b'api', '0025_auto_20150505_0926'), (b'api', '0026_contest_slug'), (b'api', '0027_auto_20150506_0816'), (b'api', '0028_contestant_slug'), (b'api', '0029_performance_slug'), (b'api', '0030_auto_20150506_0928'), (b'api', '0031_auto_20150506_0940'), (b'api', '0032_auto_20150506_1013'), (b'api', '0033_auto_20150508_0602'), (b'api', '0034_auto_20150508_0627'), (b'api', '0035_auto_20150508_0633'), (b'api', '0036_contest_district'), (b'api', '0037_convention_name'), (b'api', '0038_auto_20150508_1019'), (b'api', '0039_auto_20150508_1400'), (b'api', '0040_auto_20150509_0829'), (b'api', '0041_auto_20150509_0835'), (b'api', '0042_remove_contestant_district'), (b'api', '0043_auto_20150512_0848'), (b'api', '0044_auto_20150512_0909'), (b'api', '0045_auto_20150512_0916'), (b'api', '0046_auto_20150512_0957'), (b'api', '0047_auto_20150512_1042'), (b'api', '0048_auto_20150512_1430'), (b'api', '0049_auto_20150512_1451'), (b'api', '0050_auto_20150513_0559'), (b'api', '0051_auto_20150517_1033'), (b'api', '0052_auto_20150518_1418'), (b'api', '0053_contestant_stagetime'), (b'api', '0054_auto_20150520_1036'), (b'api', '0055_auto_20150520_1100'), (b'api', '0056_auto_20150521_1259'), (b'api', '0057_auto_20150615_0949'), (b'api', '0058_note'), (b'api', '0059_auto_20150616_1008'), (b'api', '0060_auto_20150616_1010'), (b'api', '0061_auto_20150616_1059'), (b'api', '0062_group_bsmdb_id'), (b'api', '0063_auto_20150618_1448'), (b'api', '0064_group_district_fk'), (b'api', '0065_contest_district_fk'), (b'api', '0066_contest_name'), (b'api', '0067_auto_20150618_2300'), (b'api', '0068_contestant_name'), (b'api', '0069_performance_name'), (b'api', '0070_auto_20150619_0740'), (b'api', '0071_auto_20150619_0936'), (b'api', '0072_auto_20150619_0951'), (b'api', '0073_auto_20150619_1025'), (b'api', '0074_auto_20150619_1104'), (b'api', '0075_auto_20150619_1131'), (b'api', '0076_auto_20150619_1249'), (b'api', '0077_auto_20150619_1413'), (b'api', '0078_convention_is_active'), (b'api', '0079_contest_is_active'), (b'api', '0080_contest_is_complete'), (b'api', '0081_song'), (b'api', '0082_auto_20150621_0841'), (b'api', '0083_auto_20150621_0857'), (b'api', '0084_remove_song_arrangement'), (b'api', '0085_auto_20150621_1857'), (b'api', '0086_auto_20150621_1908'), (b'api', '0087_contestant_total_raw'), (b'api', '0088_director_judge'), (b'api', '0089_auto_20150622_1359'), (b'api', '0090_contestant_district'), (b'api', '0091_remove_group_district'), (b'api', '0092_auto_20150622_2341'), (b'api', '0093_auto_20150623_0723'), (b'api', '0094_auto_20150623_0938'), (b'api', '0095_auto_20150623_0943'), (b'api', '0096_auto_20150623_1407'), (b'api', '0097_remove_district_abbr'), (b'api', '0098_auto_20150623_1423'), (b'api', '0099_auto_20150623_1431'), (b'api', '0100_contestant_men'), (b'api', '0101_remove_performance_men'), (b'api', '0102_auto_20150623_1608'), (b'api', '0103_auto_20150624_1354'), (b'api', '0104_auto_20150625_1424'), (b'api', '0105_song_slug'), (b'api', '0106_auto_20150625_2344'), (b'api', '0107_auto_20150626_0037'), (b'api', '0108_auto_20150626_0835'), (b'api', '0109_auto_20150626_0854'), (b'api', '0110_auto_20150626_1008'), (b'api', '0111_auto_20150627_2053'), (b'api', '0112_auto_20150628_1259'), (b'api', '0113_auto_20150630_1249'), (b'api', '0114_person'), (b'api', '0115_auto_20150701_1051'), (b'api', '0116_contestant_picture'), (b'api', '0117_auto_20150701_1149'), (b'api', '0118_auto_20150701_1246'), (b'api', '0119_auto_20150701_1254'), (b'api', '0120_auto_20150701_1259'), (b'api', '0121_auto_20150701_2137'), (b'api', '0122_auto_20150701_2228'), (b'api', '0123_remove_contest_is_score'), (b'api', '0124_auto_20150703_1008'), (b'api', '0125_auto_20150703_2013'), (b'api', '0126_auto_20150705_1440'), (b'api', '0127_performance'), (b'api', '0128_auto_20150706_0619'), (b'api', '0129_auto_20150706_1615'), (b'api', '0130_auto_20150706_1616'), (b'api', '0131_auto_20150707_0353'), (b'api', '0132_auto_20150707_0354'), (b'api', '0133_auto_20150707_0441'), (b'api', '0134_auto_20150707_0451'), (b'api', '0135_auto_20150707_0538'), (b'api', '0136_auto_20150707_0921'), (b'api', '0137_auto_20150707_0930'), (b'api', '0138_auto_20150707_0942'), (b'api', '0139_arranger'), (b'api', '0140_auto_20150707_1059'), (b'api', '0141_auto_20150707_1626'), (b'api', '0142_auto_20150708_0504'), (b'api', '0143_auto_20150708_0507'), (b'api', '0144_auto_20150714_1934'), (b'api', '0145_auto_20150714_1939'), (b'api', '0146_auto_20150714_2129'), (b'api', '0147_auto_20150714_2139'), (b'api', '0148_chart'), (b'api', '0149_performance_chart'), (b'api', '0150_auto_20150715_1247')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
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
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
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
                ('awards', models.ManyToManyField(related_name='groups', through='api.GroupAward', to=b'api.Award')),
                ('district', models.ForeignKey(related_name='groups', blank=True, to='api.District', help_text=b'\n            This is the district the group is officially representing in the contest.', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupFinish',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('place', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49)])),
                ('prelim', models.FloatField(null=True, blank=True)),
                ('seed', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49)])),
                ('score', models.FloatField(null=True, blank=True)),
                ('contest', models.ForeignKey(blank=True, to='api.Contest', null=True)),
                ('group', models.ForeignKey(related_name='finishes', blank=True, to='api.Group', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
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
                ('group', models.ForeignKey(related_name='performances', to='api.Group')),
                ('men', models.IntegerField(default=4, help_text=b'\n            Men on stage.', null=True, blank=True)),
                ('session', models.IntegerField(default=1, null=True, blank=True, choices=[(1, 1), (2, 2)])),
            ],
            options={
                'ordering': ['-contest', 'round', 'group'],
            },
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
        migrations.AlterModelOptions(
            name='groupfinish',
            options={'ordering': ('seed',)},
        ),
        migrations.RemoveField(
            model_name='contest',
            name='csv_finals',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='csv_quarters',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='csv_semis',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='scoresheet',
        ),
        migrations.AddField(
            model_name='contest',
            name='scoresheet_csv',
            field=models.FileField(null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
        migrations.AddField(
            model_name='contest',
            name='scoresheet_pdf',
            field=models.FileField(null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='year',
            field=models.IntegerField(default=2015, choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='year',
            field=models.IntegerField(default=2015, choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)]),
        ),
        migrations.AlterUniqueTogether(
            name='convention',
            unique_together=set([('district', 'kind', 'year')]),
        ),
        migrations.AlterUniqueTogether(
            name='contest',
            unique_together=set([('kind', 'convention', 'year', 'district')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(to='api.Convention'),
        ),
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(default=1, choices=[(1, b'Summer'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (5, b'Pan-Pacific')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(related_name='contests', to='api.Convention'),
        ),
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['-contest', 'round', 'queue', 'group']},
        ),
        migrations.RemoveField(
            model_name='groupfinish',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='groupfinish',
            name='group',
        ),
        migrations.CreateModel(
            name='Appearance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('seed', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49)])),
                ('prelim', models.FloatField(null=True, blank=True)),
                ('place', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49)])),
                ('score', models.FloatField(null=True, blank=True)),
                ('contest', models.ForeignKey(to='api.Contest')),
                ('group', models.ForeignKey(related_name='finishes', to='api.Group')),
            ],
            options={
                'ordering': ('seed',),
            },
        ),
        migrations.DeleteModel(
            name='GroupFinish',
        ),
        migrations.AddField(
            model_name='performance',
            name='appearance',
            field=models.ForeignKey(blank=True, to='api.Appearance', null=True),
        ),
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['round']},
        ),
        migrations.RemoveField(
            model_name='performance',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='group',
        ),
        migrations.AlterField(
            model_name='performance',
            name='appearance',
            field=models.ForeignKey(to='api.Appearance'),
        ),
        migrations.AlterModelOptions(
            name='appearance',
            options={'ordering': ('contest', 'group', 'place', 'seed')},
        ),
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['appearance', 'round', 'queue']},
        ),
        migrations.AlterField(
            model_name='appearance',
            name='contest',
            field=models.ForeignKey(related_name='appearances', to='api.Contest'),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='group',
            field=models.ForeignKey(related_name='appearances', to='api.Group'),
        ),
        migrations.AlterField(
            model_name='performance',
            name='appearance',
            field=models.ForeignKey(related_name='performances', to='api.Appearance'),
        ),
        migrations.AlterUniqueTogether(
            name='appearance',
            unique_together=set([('group', 'contest')]),
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('appearance', 'round', 'queue')]),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='place',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='seed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('seed', models.IntegerField(null=True, blank=True)),
                ('prelim', models.FloatField(null=True, blank=True)),
                ('place', models.IntegerField(null=True, blank=True)),
                ('score', models.FloatField(null=True, blank=True)),
                ('contest', models.ForeignKey(related_name='contestants', to='api.Contest')),
                ('group', models.ForeignKey(related_name='contestants', to='api.Group')),
            ],
            options={
                'ordering': ('contest', 'group', 'place', 'seed'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='appearance',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='appearance',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='appearance',
            name='group',
        ),
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['contestant', 'round', 'queue']},
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='performance',
            name='appearance',
        ),
        migrations.AddField(
            model_name='performance',
            name='contestant',
            field=models.ForeignKey(related_name='performances', blank=True, to='api.Contestant', null=True),
        ),
        migrations.DeleteModel(
            name='Appearance',
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('group', 'contest')]),
        ),
        migrations.AlterModelOptions(
            name='contest',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='contest',
            unique_together=set([('kind', 'convention')]),
        ),
        migrations.RemoveField(
            model_name='contest',
            name='district',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='year',
        ),
        migrations.AddField(
            model_name='contest',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, editable=False),
        ),
        migrations.AddField(
            model_name='contestant',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, editable=False),
        ),
        migrations.AddField(
            model_name='performance',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, editable=False),
        ),
        migrations.AlterField(
            model_name='performance',
            name='round',
            field=models.IntegerField(default=1, choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')]),
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('contestant', 'round')]),
        ),
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('-contest', 'group', 'place', 'seed')},
        ),
        migrations.AddField(
            model_name='contest',
            name='level',
            field=models.IntegerField(default=1, choices=[(1, b'International'), (2, b'District'), (3, b'Regional')]),
        ),
        migrations.AddField(
            model_name='contest',
            name='year',
            field=models.IntegerField(default=2015, choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)]),
        ),
        migrations.AddField(
            model_name='contest',
            name='district',
            field=models.IntegerField(blank=True, null=True, choices=[(0, b'BHS'), (1, b'CAR'), (2, b'CSD'), (3, b'DIX'), (4, b'EVG'), (5, b'FWD'), (6, b'ILL'), (7, b'JAD'), (8, b'LOL'), (9, b'MAD'), (10, b'NED'), (11, b'NSC'), (12, b'ONT'), (13, b'PIO'), (14, b'RMD'), (15, b'SLD'), (16, b'SUN'), (17, b'SWD'), (18, b'BABS'), (19, b'BHA'), (20, b'BHNZ'), (21, b'BING'), (22, b'DABS'), (23, b'FABS'), (24, b'IABS'), (25, b'NZABS'), (26, b'SABS'), (27, b'SNOBS'), (28, b'SPATS')]),
        ),
        migrations.AddField(
            model_name='convention',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the convention.', unique=True, max_length=200),
        ),
        migrations.AlterModelOptions(
            name='contest',
            options={'ordering': ('level', 'kind', 'year', 'district')},
        ),
        migrations.AlterField(
            model_name='convention',
            name='district',
            field=models.ForeignKey(blank=True, to='api.District', null=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Summer'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (5, b'Pan-Pacific')]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='year',
            field=models.IntegerField(default=2015, null=True, blank=True, choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)]),
        ),
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('-contest', '-score', '-prelim', 'group')},
        ),
        migrations.AddField(
            model_name='group',
            name='chapter_code',
            field=models.CharField(help_text=b'\n            The code of the director(s) of the chorus.', max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='chapter_name',
            field=models.CharField(help_text=b'\n            The name of the director(s) of the chorus.', max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='director',
            field=models.CharField(help_text=b'\n            The name of the director(s) of the chorus.', max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='kind',
            field=models.IntegerField(default=1, choices=[(1, b'Quartet'), (2, b'Chorus')]),
        ),
        migrations.AddField(
            model_name='group',
            name='baritone',
            field=models.ForeignKey(related_name='baritone_groups', blank=True, to='api.Singer', help_text=b'Baritone', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='bass',
            field=models.ForeignKey(related_name='bass_groups', blank=True, to='api.Singer', help_text=b'Bass', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='lead',
            field=models.ForeignKey(related_name='lead_groups', blank=True, to='api.Singer', help_text=b'Lead', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='tenor',
            field=models.ForeignKey(related_name='tenor_groups', blank=True, to='api.Singer', help_text=b'Tenor', null=True),
        ),
        migrations.AlterModelOptions(
            name='contest',
            options={'ordering': ('level', 'kind', '-year', 'district')},
        ),
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('-contest', 'place', '-score', '-prelim', 'group')},
        ),
        migrations.AlterModelOptions(
            name='convention',
            options={'ordering': ['district', '-year']},
        ),
        migrations.AddField(
            model_name='performance',
            name='mus1_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='mus2_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='prs1_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='prs2_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='sng1_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='sng2_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='song1_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='song1_raw',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='song2_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='song2_raw',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='total_rata',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='total_raw',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='session',
            field=models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2)]),
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('-contest', 'place', '-score')},
        ),
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['contestant', 'round', 'queue', 'stagetime']},
        ),
        migrations.AddField(
            model_name='contestant',
            name='stagetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_place',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_place',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='queue',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_place',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='total_rata',
            new_name='score',
        ),
        migrations.RemoveField(
            model_name='group',
            name='district',
        ),
        migrations.AlterField(
            model_name='contest',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('text', models.TextField()),
                ('performance', models.ForeignKey(to='api.Performance')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='note',
            unique_together=set([('performance', 'user')]),
        ),
        migrations.AlterField(
            model_name='note',
            name='user',
            field=models.ForeignKey(related_name='notes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contest',
            name='year',
            field=models.IntegerField(default=2015, choices=[(1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='year',
            field=models.IntegerField(default=2015, null=True, blank=True, choices=[(1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)]),
        ),
        migrations.AddField(
            model_name='contest',
            name='district_fk',
            field=models.ForeignKey(blank=True, to='api.District', null=True),
        ),
        migrations.AddField(
            model_name='contest',
            name='name',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='contest',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(related_name='contests', blank=True, to='api.Convention', null=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'International'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (5, b'Pan-Pacific')]),
        ),
        migrations.AlterUniqueTogether(
            name='contest',
            unique_together=set([]),
        ),
        migrations.AlterModelOptions(
            name='contest',
            options={'ordering': ('level', 'kind', '-year')},
        ),
        migrations.RemoveField(
            model_name='contest',
            name='district',
        ),
        migrations.RenameField(
            model_name='contest',
            old_name='district_fk',
            new_name='district',
        ),
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'International'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (5, b'Pacific')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='level',
            field=models.IntegerField(default=1, choices=[(1, b'International'), (2, b'District'), (3, b'Regional'), (4, b'Prelims')]),
        ),
        migrations.AddField(
            model_name='convention',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contest',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contest',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('is_medley', models.BooleanField(default=False)),
                ('is_parody', models.BooleanField(default=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='performance',
            name='title1',
            field=models.ForeignKey(related_name='performances_song1', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='title2',
            field=models.ForeignKey(related_name='performances_song2', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'\n            The phone number of the resource.  Include country code.', max_length=128, null=True, blank=True),
        ),
        migrations.RemoveField(
            model_name='performance',
            name='slug',
        ),
        migrations.AddField(
            model_name='contestant',
            name='points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='baritone',
            field=models.ForeignKey(related_name='contestants_baritone', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='bass',
            field=models.ForeignKey(related_name='contestants_bass', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='director',
            field=models.ForeignKey(related_name='contestants', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Director', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='lead',
            field=models.ForeignKey(related_name='contestants_lead', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='tenor',
            field=models.ForeignKey(related_name='contestants_tenor', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='district',
            field=models.ForeignKey(related_name='contestants', blank=True, to='api.District', null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='year',
            field=models.IntegerField(default=2015, choices=[(1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='year',
            field=models.IntegerField(default=2015, null=True, blank=True, choices=[(1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)]),
        ),
        migrations.RemoveField(
            model_name='group',
            name='baritone',
        ),
        migrations.RemoveField(
            model_name='group',
            name='bass',
        ),
        migrations.RemoveField(
            model_name='group',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='group',
            name='tenor',
        ),
        migrations.AddField(
            model_name='group',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contest',
            name='year',
            field=models.IntegerField(default=2015, choices=[(2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981), (1980, 1980), (1979, 1979), (1978, 1978), (1977, 1977), (1976, 1976), (1975, 1975), (1974, 1974), (1973, 1973), (1972, 1972), (1971, 1971), (1970, 1970), (1969, 1969), (1968, 1968), (1967, 1967), (1966, 1966), (1965, 1965), (1964, 1964), (1963, 1963), (1962, 1962), (1961, 1961), (1960, 1960), (1959, 1959), (1958, 1958), (1957, 1957), (1956, 1956), (1955, 1955), (1954, 1954), (1953, 1953), (1952, 1952), (1951, 1951), (1950, 1950), (1949, 1949), (1948, 1948), (1947, 1947), (1946, 1946), (1945, 1945), (1944, 1944), (1943, 1943), (1942, 1942), (1941, 1941), (1940, 1940), (1939, 1939)]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='year',
            field=models.IntegerField(default=2015, null=True, blank=True, choices=[(2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981), (1980, 1980), (1979, 1979), (1978, 1978), (1977, 1977), (1976, 1976), (1975, 1975), (1974, 1974), (1973, 1973), (1972, 1972), (1971, 1971), (1970, 1970), (1969, 1969), (1968, 1968), (1967, 1967), (1966, 1966), (1965, 1965), (1964, 1964), (1963, 1963), (1962, 1962), (1961, 1961), (1960, 1960), (1959, 1959), (1958, 1958), (1957, 1957), (1956, 1956), (1955, 1955), (1954, 1954), (1953, 1953), (1952, 1952), (1951, 1951), (1950, 1950), (1949, 1949), (1948, 1948), (1947, 1947), (1946, 1946), (1945, 1945), (1944, 1944), (1943, 1943), (1942, 1942), (1941, 1941), (1940, 1940), (1939, 1939)]),
        ),
        migrations.AlterUniqueTogether(
            name='contest',
            unique_together=set([('level', 'kind', 'year', 'district')]),
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='total_raw',
            new_name='points',
        ),
        migrations.RemoveField(
            model_name='group',
            name='director',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='mus1_rata',
            new_name='mus1_score',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='mus2_rata',
            new_name='mus2_score',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='prs1_rata',
            new_name='prs1_score',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='prs2_rata',
            new_name='prs2_score',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='sng1_rata',
            new_name='sng1_score',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='sng2_rata',
            new_name='sng2_score',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='song1_raw',
            new_name='song1_points',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='song1_rata',
            new_name='song1_score',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='song2_raw',
            new_name='song2_points',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='song2_rata',
            new_name='song2_score',
        ),
        migrations.AddField(
            model_name='contestant',
            name='men',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.RemoveField(
            model_name='performance',
            name='men',
        ),
        migrations.AlterField(
            model_name='group',
            name='chapter_name',
            field=models.CharField(help_text=b'\n            The name of the director(s) of the chorus.', max_length=200, null=True, blank=True),
        ),
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('-contest__year', 'place', '-score')},
        ),
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['contestant', 'round', 'draw', 'stagetime']},
        ),
        migrations.RenameField(
            model_name='contestant',
            old_name='queue',
            new_name='draw',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='queue',
            new_name='draw',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_score',
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_mus1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_mus1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_mus2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_mus2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_prs1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_prs1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_prs2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_prs2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_sng1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_sng1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_sng2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_sng2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song1',
            field=models.ForeignKey(related_name='contestants_finals_song1', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song2',
            field=models.ForeignKey(related_name='contestants_finals_song2', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_mus1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_mus1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_mus2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_mus2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_prs1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_prs1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_prs2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_prs2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_sng1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_sng1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_sng2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_sng2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song1',
            field=models.ForeignKey(related_name='contestants_quarters_song1', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song2',
            field=models.ForeignKey(related_name='contestants_quarters_song2', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_mus1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_mus1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_mus2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_mus2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_prs1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_prs1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_prs2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_prs2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_sng1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_sng1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_sng2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_sng2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song1',
            field=models.ForeignKey(related_name='contestants_semis_song1', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song1_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song1_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song2',
            field=models.ForeignKey(related_name='contestants_semis_song2', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song2_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song2_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterModelOptions(
            name='contest',
            options={'ordering': ('level', '-year', 'kind')},
        ),
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='contest',
            name='is_place',
            field=models.BooleanField(default=False),
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
        migrations.AddField(
            model_name='contestant',
            name='picture',
            field=models.ImageField(help_text=b'\n            The picture/logo of the resource.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='baritone',
            field=models.ForeignKey(related_name='contestants_baritone', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='bass',
            field=models.ForeignKey(related_name='contestants_bass', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='director',
            field=models.ForeignKey(related_name='contestants_director', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='lead',
            field=models.ForeignKey(related_name='contestants_lead', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='tenor',
            field=models.ForeignKey(related_name='contestants_tenor', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song1_arranger',
            field=models.ForeignKey(related_name='contestants_f1_arranger', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_song2_arranger',
            field=models.ForeignKey(related_name='contestants_f2_arranger', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song1_arranger',
            field=models.ForeignKey(related_name='contestants_quarters_song1_arranger', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_song2_arranger',
            field=models.ForeignKey(related_name='contestants_quarters_song2_arranger', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song1_arranger',
            field=models.ForeignKey(related_name='contestants_semis_song1_arranger', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_song2_arranger',
            field=models.ForeignKey(related_name='contestants_semis_song2_arranger', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='note',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='note',
            name='performance',
        ),
        migrations.RemoveField(
            model_name='note',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='performance',
            name='contestant',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='title1',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='title2',
        ),
        migrations.DeleteModel(
            name='Note',
        ),
        migrations.DeleteModel(
            name='Performance',
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True)),
                ('round', models.IntegerField(default=3, null=True, blank=True, choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')])),
                ('order', models.IntegerField(blank=True, null=True, choices=[(1, b'1'), (2, b'2')])),
                ('mus_points', models.IntegerField(null=True, blank=True)),
                ('prs_points', models.IntegerField(null=True, blank=True)),
                ('sng_points', models.IntegerField(null=True, blank=True)),
                ('total_points', models.IntegerField(null=True, blank=True)),
                ('mus_score', models.FloatField(null=True, blank=True)),
                ('prs_score', models.FloatField(null=True, blank=True)),
                ('sng_score', models.FloatField(null=True, blank=True)),
                ('total_score', models.FloatField(null=True, blank=True)),
                ('penalty', models.TextField(null=True, blank=True)),
                ('arranger', models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True)),
                ('contestant', models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Contestant', null=True)),
                ('song', models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Song', null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['contestant', 'round', 'order']},
        ),
        migrations.AlterField(
            model_name='performance',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, populate_from=b'name', null=True, editable=False, blank=True),
        ),
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True)),
                ('part', models.IntegerField(blank=True, null=True, choices=[(1, b'Tenor'), (2, b'Lead'), (3, b'Baritone'), (4, b'Bass')])),
                ('contestant', models.ForeignKey(related_name='singers', to='api.Contestant')),
                ('person', models.ForeignKey(related_name='quartets', to='api.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True)),
                ('part', models.IntegerField(default=1, choices=[(1, b'Director'), (2, b'Co-Director')])),
                ('contestant', models.ForeignKey(related_name='directors', to='api.Contestant')),
                ('person', models.ForeignKey(related_name='choruses', to='api.Person')),
            ],
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='baritone',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='bass',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='director',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_mus1_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_mus1_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_mus2_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_mus2_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_prs1_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_prs1_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_prs2_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_prs2_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_sng1_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_sng1_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_sng2_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_sng2_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_song1',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_song1_arranger',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_song1_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_song1_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_song2',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_song2_arranger',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_song2_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_song2_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_mus1_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_mus1_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_mus2_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_mus2_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_prs1_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_prs1_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_prs2_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_prs2_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_sng1_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_sng1_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_sng2_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_sng2_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_song1',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_song1_arranger',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_song1_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_song1_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_song2',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_song2_arranger',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_song2_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_song2_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_mus1_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_mus1_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_mus2_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_mus2_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_prs1_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_prs1_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_prs2_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_prs2_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_sng1_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_sng1_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_sng2_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_sng2_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_song1',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_song1_arranger',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_song1_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_song1_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_song2',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_song2_arranger',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_song2_points',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_song2_score',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='tenor',
        ),
        migrations.AlterField(
            model_name='performance',
            name='contestant',
            field=models.ForeignKey(related_name='performances', to='api.Contestant'),
        ),
        migrations.AlterField(
            model_name='performance',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='performance',
            name='order',
            field=models.IntegerField(choices=[(1, b'1'), (2, b'2')]),
        ),
        migrations.AlterField(
            model_name='performance',
            name='round',
            field=models.IntegerField(choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')]),
        ),
        migrations.AlterField(
            model_name='performance',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(related_name='contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Convention', null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='level',
            field=models.IntegerField(default=1, choices=[(1, b'International')]),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='district',
            field=models.ForeignKey(related_name='contestants', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', null=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', null=True),
        ),
        migrations.RemoveField(
            model_name='group',
            name='awards',
        ),
        migrations.AlterField(
            model_name='contestant',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
        migrations.AddField(
            model_name='convention',
            name='end',
            field=models.DateTimeField(null=True, verbose_name='end', blank=True),
        ),
        migrations.AddField(
            model_name='convention',
            name='start',
            field=models.DateTimeField(null=True, verbose_name='start', blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='end',
            field=models.DateTimeField(null=True, verbose_name='end', blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='start',
            field=models.DateTimeField(null=True, verbose_name='start', blank=True),
        ),
        migrations.AddField(
            model_name='contest',
            name='status',
            field=model_utils.fields.StatusField(default=b'Upcoming', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(0, 'dummy')]),
        ),
        migrations.AddField(
            model_name='contest',
            name='status_changed',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status'),
        ),
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True)),
                ('arranger', models.ForeignKey(related_name='charts', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True)),
                ('song', models.ForeignKey(related_name='charts', to='api.Song')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='performance',
            name='chart',
            field=models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Chart', null=True),
        ),
        migrations.RemoveField(
            model_name='performance',
            name='arranger',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='song',
        ),
    ]
