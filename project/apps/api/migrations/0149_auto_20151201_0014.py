# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0148_auto_20151201_0013'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='panel',
            field=models.ForeignKey(related_name='sessions', blank=True, to='api.Panel', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('group', 'contest')]),
        ),
        migrations.AlterUniqueTogether(
            name='day',
            unique_together=set([('contest', 'kind')]),
        ),
        migrations.AlterUniqueTogether(
            name='panelist',
            unique_together=set([('contest', 'category', 'slot'), ('contest', 'person')]),
        ),
    ]
