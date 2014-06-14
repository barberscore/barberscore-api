# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0023_auto_20140613_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='sng1',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='prs1',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='sng2',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='mus1',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='mus2',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='prs2',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
