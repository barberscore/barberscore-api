# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0119_auto_20150701_1254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contestant',
            old_name='P_director',
            new_name='director',
        ),
        migrations.RenameField(
            model_name='contestant',
            old_name='P_tenor',
            new_name='tenor',
        ),
        migrations.RenameField(
            model_name='contestant',
            old_name='P_lead',
            new_name='lead',
        ),
        migrations.RenameField(
            model_name='contestant',
            old_name='P_baritone',
            new_name='baritone',
        ),
        migrations.RenameField(
            model_name='contestant',
            old_name='P_bass',
            new_name='bass',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='P_director',
            new_name='director',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='P_tenor',
            new_name='tenor',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='P_lead',
            new_name='lead',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='P_baritone',
            new_name='baritone',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='P_bass',
            new_name='bass',
        ),
    ]
