# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0134_remove_ranking_contest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='convention',
            options={'ordering': ['-year', 'organization__name']},
        ),
        migrations.AlterField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(related_name='contests', to='api.Convention', help_text=b'\n            The convention at which this contest occurred.'),
        ),
    ]
