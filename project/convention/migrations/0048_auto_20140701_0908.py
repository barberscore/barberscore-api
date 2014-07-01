# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0047_auto_20140623_1347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contest',
            options={'ordering': (b'-year', b'contest_level', b'contest_type')},
        ),
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': [b'contestant_type', b'name']},
        ),
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': (b'contest', b'contest_round', b'appearance')},
        ),
        migrations.AddField(
            model_name='contestant',
            name='district_id',
            field=models.IntegerField(default=0, help_text=b'\n            The district the\n            contestant is representing.', choices=[(0, b'UNK'), (1, b'CAR'), (2, b'CSD'), (3, b'DIX'), (4, b'EVG'), (5, b'FWD'), (6, b'ILL'), (7, b'JAD'), (8, b'LOL'), (9, b'MAD'), (10, b'NED'), (11, b'NSC'), (12, b'ONT'), (13, b'PIO'), (14, b'RMD'), (15, b'SLD'), (16, b'SUN'), (17, b'SWD'), (18, b'BABS'), (19, b'BHA'), (20, b'NZABS'), (21, b'SNOBS')]),
            preserve_default=True,
        ),
    ]
