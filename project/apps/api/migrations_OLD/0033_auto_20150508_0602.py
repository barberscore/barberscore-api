# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_auto_20150506_1013'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('-contest', 'group', 'place', 'seed')},
        ),
        migrations.AddField(
            model_name='group',
            name='district_tag',
            field=models.IntegerField(default=0, choices=[(0, b'BHS'), (1, b'CAR'), (2, b'CSD'), (3, b'DIX'), (4, b'EVG'), (5, b'FWD'), (6, b'ILL'), (7, b'JAD'), (8, b'LOL'), (9, b'MAD'), (10, b'NED'), (11, b'NSC'), (12, b'ONT'), (13, b'PIO'), (14, b'RMD'), (15, b'SLD'), (16, b'SUN'), (17, b'SWD'), (18, b'BABS'), (19, b'BHA'), (20, b'BING'), (21, b'DABS'), (22, b'FABS'), (23, b'IABS'), (24, b'NZABS'), (25, b'SABS'), (26, b'SNOBS'), (27, b'SPATS')]),
        ),
    ]
