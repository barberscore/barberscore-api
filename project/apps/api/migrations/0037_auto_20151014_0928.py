# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20151014_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='draw',
            field=models.IntegerField(help_text=b'\n            The OA (Order of Appearance) in the contest schedule.  Specific to each round/session.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='stagetime',
            field=models.DateTimeField(help_text=b"\n            The estimated stagetime (may be replaced by 'start' in later versions).", null=True, blank=True),
        ),
    ]
