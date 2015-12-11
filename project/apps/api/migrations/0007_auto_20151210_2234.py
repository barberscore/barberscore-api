# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20151210_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(blank=True, help_text=b'\n            Most persons are individuals; however, they can be grouped into teams for the purpose of multi-arranger songs.', null=True, choices=[(b'International', [(10, b'International'), (15, b'Midwinter')]), (b'District', [(20, b'CAR'), (30, b'CSD'), (40, b'DIX'), (50, b'EVG'), (60, b'FWD'), (70, b'ILL'), (80, b'JAD'), (90, b'LOL'), (100, b'MAD'), (110, b'NED'), (120, b'NSC'), (130, b'ONT'), (140, b'PIO'), (150, b'RMD'), (160, b'SLD'), (170, b'SUN'), (180, b'SWD'), (190, b'District')]), (b'Division', [(200, b'Evergreen District Division I'), (210, b'Evergreen District Division II'), (220, b'Evergreen District Division III'), (230, b'Evergreen District Division IV'), (240, b'Evergreen District Division V'), (250, b'Far Western District Arizona Division'), (260, b'Far Western District NE/NW Division'), (270, b'Far Western District SE/SW Division'), (280, b"Land O' Lakes District Division One/Packerland Division"), (290, b"Land O' Lakes District Northern Plains Division"), (300, b"Land O' Lakes District 10,000 Lakes and Southwest Division"), (310, b'Mid-Atlantic District Atlantic Division'), (320, b'Mid-Atlantic District Northern and Western Division'), (330, b'Mid-Atlantic District Southern Division')])]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='season',
            field=models.IntegerField(help_text=b'\n            The kind of convention.', choices=[(1, b'International'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (9, b'Video')]),
        ),
    ]
