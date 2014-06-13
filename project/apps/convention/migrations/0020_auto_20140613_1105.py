# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0019_auto_20140612_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='seed',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='performance',
            name='song1_score',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='performance',
            name='song2_score',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contestant',
            name='score',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contestant',
            name='rank',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='performance',
            name='performance_score',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
