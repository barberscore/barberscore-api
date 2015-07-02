# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0121_auto_20150701_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name='finals_draw',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='finals_stagetime',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_draw',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='quarters_stagetime',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_draw',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='semis_stagetime',
        ),
    ]
