# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20150421_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='quartet',
            name='baritone',
            field=models.ForeignKey(related_name='quartet_baritones', blank=True, to='api.Singer', help_text=b'Baritone', null=True),
        ),
        migrations.AddField(
            model_name='quartet',
            name='bass',
            field=models.ForeignKey(related_name='quartet_basses', blank=True, to='api.Singer', help_text=b'Bass', null=True),
        ),
        migrations.AddField(
            model_name='quartet',
            name='lead',
            field=models.ForeignKey(related_name='quartet_leads', blank=True, to='api.Singer', help_text=b'Lead', null=True),
        ),
        migrations.AddField(
            model_name='quartet',
            name='tenor',
            field=models.ForeignKey(related_name='quartet_tenors', blank=True, to='api.Singer', help_text=b'Tenor', null=True),
        ),
    ]
