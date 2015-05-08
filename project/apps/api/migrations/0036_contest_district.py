# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_auto_20150508_0633'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='district',
            field=models.IntegerField(blank=True, null=True, choices=[(0, b'BHS'), (1, b'CAR'), (2, b'CSD'), (3, b'DIX'), (4, b'EVG'), (5, b'FWD'), (6, b'ILL'), (7, b'JAD'), (8, b'LOL'), (9, b'MAD'), (10, b'NED'), (11, b'NSC'), (12, b'ONT'), (13, b'PIO'), (14, b'RMD'), (15, b'SLD'), (16, b'SUN'), (17, b'SWD'), (18, b'BABS'), (19, b'BHA'), (20, b'BHNZ'), (21, b'BING'), (22, b'DABS'), (23, b'FABS'), (24, b'IABS'), (25, b'NZABS'), (26, b'SABS'), (27, b'SNOBS'), (28, b'SPATS')]),
        ),
    ]
