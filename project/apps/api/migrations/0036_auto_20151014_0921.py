# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import apps.api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_auto_20151013_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(related_name='contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Convention', help_text=b'\n            The convention at which this contest occurred.', null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='kind',
            field=models.IntegerField(default=1, help_text=b'\n            The kind of the contest (quartet, chorus, senior, collegiate.)', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='level',
            field=models.IntegerField(default=1, help_text=b'\n            The level of the contest (currently only International is supported.)', choices=[(1, b'International')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='panel',
            field=models.IntegerField(default=5, help_text=b'\n            Size of the judging panel (typically three or five.)'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='scoresheet_csv',
            field=models.FileField(help_text=b'\n            The parsed scoresheet (used for legacy imports).', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='scoresheet_pdf',
            field=models.FileField(help_text=b'\n            PDF of the OSS.', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='district',
            field=models.ForeignKey(related_name='contestants', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', help_text=b'\n            The district this contestant is representing.', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='draw',
            field=models.IntegerField(help_text=b'\n            The OA (Order of Appearance) in the contest schedule.  Specific to each round/session.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='finals_place',
            field=models.IntegerField(help_text=b'\n            The place for the fainal round/session.  This is for the finals only and is NOT cumulative.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='finals_points',
            field=models.IntegerField(help_text=b'\n            The total points for the final round/session.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='finals_score',
            field=models.FloatField(help_text=b'\n            The percential score for the final round/session.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='men',
            field=models.IntegerField(help_text=b'\n            The number of men on stage (only for chourses).', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='picture',
            field=models.ImageField(help_text=b'\n            The performance picture (as opposed to the "official" photo).', null=True, upload_to=apps.api.models.generate_image_filename, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='place',
            field=models.IntegerField(help_text=b'\n            The final placement/rank of the contestant.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='points',
            field=models.IntegerField(help_text=b'\n            Total raw points for the contest.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='prelim',
            field=models.FloatField(help_text=b'\n            The incoming prelim score.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='quarters_place',
            field=models.IntegerField(help_text=b'\n            The place for the quarterfinal round/session.  This is for the quarters only and is NOT cumulative.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='quarters_points',
            field=models.IntegerField(help_text=b'\n            The total points for the quarterfinal round/session.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='quarters_score',
            field=models.FloatField(help_text=b'\n            The percential score for the quarterfinal round/session.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='score',
            field=models.FloatField(help_text=b'\n            The percentile of the total points.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='seed',
            field=models.IntegerField(help_text=b'\n            The incoming rank based on prelim score.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='semis_place',
            field=models.IntegerField(help_text=b'\n            The place for the semifinal round/session.  This is for the semis only and is NOT cumulative.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='semis_points',
            field=models.IntegerField(help_text=b'\n            The total points for the semifinal round/session.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='semis_score',
            field=models.FloatField(help_text=b'\n            The percential score for the semifinal round/session.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='stagetime',
            field=models.DateTimeField(help_text=b"\n            The estimated stagetime (may be replaced by 'start' in later versions).", null=True, blank=True),
        ),
    ]
