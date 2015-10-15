# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_auto_20151015_0957'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['contestant', 'session', 'order']},
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='round',
            new_name='session',
        ),
        migrations.AlterField(
            model_name='contestant',
            name='finals_place',
            field=models.IntegerField(help_text=b'\n            The place for the fainal session.  This is for the finals only and is NOT cumulative.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='finals_points',
            field=models.IntegerField(help_text=b'\n            The total points for the final session.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='finals_score',
            field=models.FloatField(help_text=b'\n            The percential score for the final session.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='quarters_place',
            field=models.IntegerField(help_text=b'\n            The place for the quarterfinal session.  This is for the quarters only and is NOT cumulative.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='quarters_points',
            field=models.IntegerField(help_text=b'\n            The total points for the quarterfinal session.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='quarters_score',
            field=models.FloatField(help_text=b'\n            The percential score for the quarterfinal session.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='score',
            field=models.FloatField(help_text=b'\n            The percentile of the total points (cumulative , all sessions).', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='semis_place',
            field=models.IntegerField(help_text=b'\n            The place for the semifinal session.  This is for the semis only and is NOT cumulative.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='semis_points',
            field=models.IntegerField(help_text=b'\n            The total points for the semifinal session.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='semis_score',
            field=models.FloatField(help_text=b'\n            The percential score for the semifinal session.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='draw',
            field=models.IntegerField(help_text=b'\n            The OA (Order of Appearance) in the contest schedule.  Specific to each session.', null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('contestant', 'session', 'order')]),
        ),
    ]
