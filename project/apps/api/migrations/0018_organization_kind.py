# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20151212_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='kind',
            field=models.IntegerField(blank=True, help_text=b'\n            The kind of organization.', null=True, choices=[(0, b'International'), (10, b'District'), (20, b'Noncompetitive'), (30, b'Affiliate'), (40, b'Division'), (50, b'Harmony International')]),
        ),
    ]
