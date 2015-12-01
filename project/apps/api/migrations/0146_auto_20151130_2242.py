# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0145_auto_20151130_2212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Panel',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, editable=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Qualified'), (20, b'Accepted'), (30, b'Declined'), (40, b'Dropped'), (50, b'Official'), (60, b'Finished'), (90, b'Final')])),
                ('status_monitor', model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status')),
                ('kind', models.IntegerField(blank=True, null=True, choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate'), (5, b'Novice')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='contest',
            old_name='panel',
            new_name='panel_size',
        ),
        migrations.AddField(
            model_name='award',
            name='convention',
            field=models.ForeignKey(related_name='awards', blank=True, to='api.Convention', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='convention',
            field=models.ForeignKey(related_name='contestants', blank=True, to='api.Convention', null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='convention',
            field=models.ForeignKey(related_name='sessions', blank=True, to='api.Convention', null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='contest',
            field=models.ForeignKey(related_name='panel', to='api.Contest'),
        ),
        migrations.AddField(
            model_name='panel',
            name='convention',
            field=models.ForeignKey(related_name='panel', blank=True, to='api.Convention', null=True),
        ),
        migrations.AddField(
            model_name='panelist',
            name='panel',
            field=models.ForeignKey(related_name='panelists', blank=True, to='api.Panel', null=True),
        ),
    ]
