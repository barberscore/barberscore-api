# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0027_contestant_twitter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='session',
            field=models.IntegerField(blank=True, help_text=b'\n            Contest rounds are broken down into sessions, which\n            are tracked here.', null=True, choices=[(1, b'Collegiate Finals'), (2, b'Quartet Quarter-Finals Session #1'), (3, b'Quartet Quarter-Finals Session #2'), (4, b'Chorus Finals Session #1'), (5, b'Chorus Finals Session #2'), (6, b'Quartet Semi-Finals'), (7, b'Quartet Finals')]),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='baritone',
            field=models.CharField(help_text=b'\n            The name of the quartet baritone.', max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='contestant_type',
            field=models.IntegerField(blank=True, help_text=b'\n            The type of contestant, either chorus or quartet.', null=True, choices=[(1, b'Quartet'), (2, b'Chorus')]),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='location',
            field=models.CharField(help_text=b'\n            The geographical location of the contestant.', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='slug',
            field=models.SlugField(help_text=b'\n            The slug of the contest type.', unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='email',
            field=models.EmailField(help_text=b'\n            The contact email of the contestant.', max_length=75, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='contest_round',
            field=models.IntegerField(default=3, help_text=b'\n            The performance contest round.', choices=[(1, b'Quarter-Finals'), (2, b'Semi-Finals'), (3, b'Finals')]),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='tenor',
            field=models.CharField(help_text=b'\n            The name of the quartet tenor.', max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='sng1',
            field=models.IntegerField(help_text=b'\n            The raw singing score of the first song.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='slug',
            field=models.SlugField(help_text=b'\n            The slug, generated in a signal from the name field.', unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='performance',
            name='total_score',
            field=models.FloatField(help_text=b'\n            The running percentile score of performances to date\n            by this particular contestant.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='prelim',
            field=models.FloatField(help_text=b'\n            The prelim score of the contestant.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='contest_type',
            field=models.IntegerField(blank=True, help_text=b'\n            The contest type:  Quartet, Chorus, Collegiate or Senior.', null=True, choices=[(1, b'Quartet Contest'), (2, b'Chorus Contest'), (3, b'Collegiate Contest'), (4, b'Senior Contest')]),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='twitter',
            field=models.CharField(help_text=b'\n            The twitter handle (in form @twitter_handle) of the contestant.', max_length=16, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='sng2',
            field=models.IntegerField(help_text=b'\n            The raw singing score of the second song.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='performance_score',
            field=models.FloatField(help_text=b'\n            The percentile score of the performance (both songs).', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the contestant.', max_length=200),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='blurb',
            field=models.TextField(help_text=b'\n            A blurb describing the contestant.  Max 1000 characters.', max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='lead',
            field=models.CharField(help_text=b'\n            The name of the quartet lead.', max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='picture',
            field=models.ImageField(help_text=b"\n            The 'official' picture of the contestant.", null=True, upload_to=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='mus1',
            field=models.IntegerField(help_text=b'\n            The raw music score of the first song.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='song1',
            field=models.CharField(help_text=b'\n            The title of the first song of the performance.', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='website',
            field=models.URLField(help_text=b'\n            The website URL of the contestant.', blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='mus2',
            field=models.IntegerField(help_text=b'\n            The raw music score of the second song.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='song2_score',
            field=models.FloatField(help_text=b'\n            The percentile score of the second song.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='appearance',
            field=models.IntegerField(help_text=b'\n            The appearance order, within a given round.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='phone',
            field=models.CharField(help_text=b'\n            The contact phone number of the contestant.', max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='place',
            field=models.IntegerField(help_text=b'\n            The ordinal placement of the contestant in this\n            particular contest.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='director',
            field=models.CharField(help_text=b'\n            The name of the director(s) of the chorus.', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='bass',
            field=models.CharField(help_text=b'\n            The name of the quartet bass.', max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='contestant',
            field=models.ForeignKey(to_field='id', blank=True, to='convention.Contestant', help_text=b'\n            The contestant for this particular performance.', null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='stagetime',
            field=models.DateTimeField(help_text=b'\n            The approximate stagetime of the performance, in\n            the local time of the venue.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='men_on_stage',
            field=models.IntegerField(help_text=b'\n            The number of men on stage (relevant for chorus only.)', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='contest',
            field=models.ForeignKey(to_field='id', blank=True, to='convention.Contest', help_text=b'\n            The contest for this particular performance.', null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='song2',
            field=models.CharField(help_text=b'\n            The title of the second song of the performance.', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='prs1',
            field=models.IntegerField(help_text=b'\n            The raw presentation score of the first song.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='facebook',
            field=models.URLField(help_text=b'\n            The facebook URL of the contestant.', blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='district',
            field=models.CharField(help_text=b'\n            The abbreviation of the district the\n            contestant is representing.', max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='prs2',
            field=models.IntegerField(help_text=b'\n            The raw presentation score of the second song.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='song1_score',
            field=models.FloatField(help_text=b'\n            The percentile score of the first song.', null=True, blank=True),
        ),
    ]
