# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0131_entrant_convention'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entrant',
            options={'ordering': ('convention', 'group')},
        ),
        migrations.AlterUniqueTogether(
            name='entrant',
            unique_together=set([('group', 'convention')]),
        ),
    ]
