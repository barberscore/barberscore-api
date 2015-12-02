# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django_fsm
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0130_auto_20151128_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='contest',
            field=models.ForeignKey(related_name='awards', blank=True, to='api.Contest', null=True),
        ),
        migrations.AddField(
            model_name='award',
            name='kind',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate')]),
        ),
        migrations.AddField(
            model_name='award',
            name='status',
            field=django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (10, b'Qualified'), (20, b'Accepted'), (30, b'Declined'), (40, b'Dropped'), (50, b'Official'), (60, b'Finished'), (90, b'Final')]),
        ),
        migrations.AddField(
            model_name='award',
            name='status_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status'),
        ),
    ]
