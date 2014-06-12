# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0010_performance_appearance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='slug',
        ),
        migrations.AlterField(
            model_name='performance',
            name='appearance',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='sng1',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='mus2',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='mus1',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='contest',
            field=models.ForeignKey(to_field='id', blank=True, to='convention.Contest', null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='prs2',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='prs1',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='men_on_stage',
            field=models.IntegerField(default=4, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='song1',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='song2',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='contestant',
            field=models.ForeignKey(to_field='id', blank=True, to='convention.Contestant', null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='sng2',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
