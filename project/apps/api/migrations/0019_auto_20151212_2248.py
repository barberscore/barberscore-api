# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_organization_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='kind',
            field=models.IntegerField(blank=True, help_text=b'\n            The kind of organization.', null=True, choices=[(b'International', [(0, b'International'), (50, b'Harmony Incorporated')]), (b'District', [(10, b'District'), (20, b'Noncompetitive'), (30, b'Affiliate')]), (b'Division', [(40, b'Division')])]),
        ),
        migrations.AlterField(
            model_name='organization',
            name='level',
            field=models.IntegerField(blank=True, help_text=b'\n            The level of the contest.  Note that this may be different than the level of the parent session.', null=True, choices=[(0, b'International'), (1, b'District/Affiliates'), (2, b'Division')]),
        ),
    ]
