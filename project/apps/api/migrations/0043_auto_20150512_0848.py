# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_remove_contestant_district'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='district_OLD',
        ),
        migrations.AddField(
            model_name='group',
            name='baritone_2',
            field=models.ForeignKey(related_name='quartet_baritones_2', blank=True, to='api.Singer', help_text=b'Baritone', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='bass_2',
            field=models.ForeignKey(related_name='quartet_basses_2', blank=True, to='api.Singer', help_text=b'Bass', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='chapter_code_2',
            field=models.CharField(help_text=b'\n            The code of the director(s) of the chorus.', max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='chapter_name_2',
            field=models.CharField(help_text=b'\n            The name of the director(s) of the chorus.', max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='director_2',
            field=models.CharField(help_text=b'\n            The name of the director(s) of the chorus.', max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='kind',
            field=models.IntegerField(default=1, choices=[(1, b'Quartet'), (2, b'Chorus')]),
        ),
        migrations.AddField(
            model_name='group',
            name='lead_2',
            field=models.ForeignKey(related_name='quartet_leads_2', blank=True, to='api.Singer', help_text=b'Lead', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='tenor_2',
            field=models.ForeignKey(related_name='quartet_tenors_2', blank=True, to='api.Singer', help_text=b'Tenor', null=True),
        ),
    ]
