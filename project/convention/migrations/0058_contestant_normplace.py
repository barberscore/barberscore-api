# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0057_remove_contestant_running_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='normplace',
            field=models.IntegerField(help_text=b'Denormalized placement, for use in ordering. HACK', null=True, blank=True),
            preserve_default=True,
        ),
    ]
