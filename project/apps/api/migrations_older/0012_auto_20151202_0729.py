# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_contest_panel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('convention', 'group__kind', 'group')},
        ),
        migrations.AddField(
            model_name='ranking',
            name='men',
            field=models.IntegerField(default=4, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='mus_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='mus_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='place',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='prs_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='prs_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='sng_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='sng_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='total_points',
            field=models.IntegerField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ranking',
            name='total_score',
            field=models.FloatField(null=True, editable=False, blank=True),
        ),
    ]
