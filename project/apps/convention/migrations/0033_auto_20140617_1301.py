# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0032_auto_20140617_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='name',
            field=models.CharField(help_text=b'\n            The verbose name of the contest.', max_length=200),
        ),
        migrations.AlterField(
            model_name='performance',
            name='song1',
            field=models.CharField(help_text=b'\n            The title of the first song of the performance.', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='startdate',
            field=models.DateField(help_text=b'\n            The start date of the contest.'),
        ),
        migrations.AlterField(
            model_name='performance',
            name='contestant',
            field=models.ForeignKey(to='convention.Contestant', help_text=b'\n            The contestant for this particular performance.', to_field='id'),
        ),
        migrations.AlterField(
            model_name='performance',
            name='contest',
            field=models.ForeignKey(to='convention.Contest', help_text=b'\n            The contest for this particular performance.', to_field='id'),
        ),
        migrations.AlterField(
            model_name='performance',
            name='song2',
            field=models.CharField(help_text=b'\n            The title of the second song of the performance.', max_length=200, blank=True),
        ),
    ]
