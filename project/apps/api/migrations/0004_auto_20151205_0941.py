# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20151204_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The kind of the award.  Note that this may be different than the kind of the parent contest.', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate'), (5, b'Novice'), (6, b'Plateau A'), (7, b'Plateau AA'), (8, b'Plateau AAA'), (9, b"Dealer's Choice")]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The kind of convention.', choices=[(1, b'International'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (5, b'Pacific'), (6, b'Southeast and Southwest'), (7, b'Northeast and Northwest')]),
        ),
    ]
