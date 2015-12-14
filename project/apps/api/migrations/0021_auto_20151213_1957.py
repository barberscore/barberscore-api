# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20151212_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='stix_name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='convention',
            unique_together=set([('organization', 'kind', 'year', 'combo', 'stix_name')]),
        ),
    ]
