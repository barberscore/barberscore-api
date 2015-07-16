# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_auto_20150512_0909'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='chapter_code_2',
            new_name='chapter_code',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='chapter_name_2',
            new_name='chapter_name',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='director_2',
            new_name='director',
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
        migrations.AlterField(
            model_name='group',
            name='baritone_2',
            field=models.ForeignKey(related_name='baritone_leads_2', blank=True, to='api.Singer', help_text=b'Baritone', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='bass_2',
            field=models.ForeignKey(related_name='bass_leads_2', blank=True, to='api.Singer', help_text=b'Bass', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='tenor_2',
            field=models.ForeignKey(related_name='tenor_leads_2', blank=True, to='api.Singer', help_text=b'Tenor', null=True),
        ),
    ]
