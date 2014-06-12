# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0015_contestant_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='sng1',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='mus2',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='mus1',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='contest_round',
            field=models.IntegerField(default=0, choices=[(1, b'Quarter-Finals'), (2, b'Semi-Finals'), (3, b'Finals')]),
        ),
        migrations.AlterField(
            model_name='performance',
            name='prs2',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='prs1',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='sng2',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
