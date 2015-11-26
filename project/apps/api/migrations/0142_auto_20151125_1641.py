# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0141_auto_20151125_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='director',
            name='entrant',
            field=models.ForeignKey(related_name='directors', to='api.Entrant'),
        ),
        migrations.AlterField(
            model_name='singer',
            name='entrant',
            field=models.ForeignKey(related_name='singers', to='api.Entrant'),
        ),
        migrations.AlterUniqueTogether(
            name='director',
            unique_together=set([('entrant', 'person')]),
        ),
        migrations.AlterUniqueTogether(
            name='singer',
            unique_together=set([('entrant', 'person')]),
        ),
        migrations.RemoveField(
            model_name='director',
            name='contestant',
        ),
        migrations.RemoveField(
            model_name='singer',
            name='contestant',
        ),
    ]
