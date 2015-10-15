# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='contest',
            field=models.ForeignKey(related_name='events', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Contest', help_text=b'\n            The contest associated with this event.', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='contestant',
            field=models.ForeignKey(related_name='events', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Contestant', help_text=b'\n            The contestant associated with this event.', null=True),
        ),
        migrations.AlterField(
            model_name='judge',
            name='person',
            field=models.ForeignKey(related_name='contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
    ]
