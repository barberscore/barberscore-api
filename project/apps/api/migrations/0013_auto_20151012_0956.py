# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_person_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='kind',
            field=models.IntegerField(default=1, help_text=b'\n            Most persons are individuals; they can be grouped into teams for the purpose of multi-arranger songs.', choices=[(1, b'Individual'), (2, b'Team')]),
        ),
    ]
