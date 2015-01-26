# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_remove_chorusperformance_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quartetmembership',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='quartetmembership',
            name='quartet',
        ),
        migrations.RemoveField(
            model_name='quartetmembership',
            name='singer',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='members',
        ),
        migrations.DeleteModel(
            name='QuartetMembership',
        ),
        migrations.AddField(
            model_name='quartet',
            name='baritone',
            field=models.ForeignKey(related_name='quartet_baritone', blank=True, to='api.Singer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartet',
            name='bass',
            field=models.ForeignKey(related_name='quartet_bass', blank=True, to='api.Singer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartet',
            name='lead',
            field=models.ForeignKey(related_name='quartet_lead', blank=True, to='api.Singer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartet',
            name='tenor',
            field=models.ForeignKey(related_name='quartet_tenor', blank=True, to='api.Singer', null=True),
            preserve_default=True,
        ),
    ]
