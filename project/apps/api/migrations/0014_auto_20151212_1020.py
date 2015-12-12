# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_remove_performance_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The kind of the contest.  Note that this may be different than the kind of the parent session.', choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate'), (5, b'Novice'), (6, b'Plateau A'), (7, b'Plateau AA'), (8, b'Plateau AAA')]),
        ),
    ]
