# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0157_panelist_panel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='panelist',
            options={'ordering': ('panel', 'category', 'slot')},
        ),
        migrations.AlterUniqueTogether(
            name='panelist',
            unique_together=set([('panel', 'category', 'slot'), ('panel', 'person')]),
        ),
        migrations.RemoveField(
            model_name='panelist',
            name='contest',
        ),
    ]
