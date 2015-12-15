# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_session_stix_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='stix_name',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='award',
            name='stix_num',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='award',
            name='kind',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate'), (5, b'Novice')]),
        ),
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set([]),
        ),
    ]
