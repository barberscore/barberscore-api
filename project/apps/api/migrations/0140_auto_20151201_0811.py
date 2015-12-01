# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0139_ranking_contest'),
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
                ('status', models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Scheduled'), (20, b'Confirmed'), (30, b'Final')])),
                ('status_monitor', model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status')),
                ('kind', models.IntegerField(blank=True, help_text=b'\n            Most persons are individuals; however, they can be grouped into teams for the purpose of multi-arranger songs.', null=True, choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate')])),
                ('convention', models.ForeignKey(related_name='panels', to='api.Convention')),
            ],
            options={
                'ordering': ('convention', 'kind'),
            },
        ),
        migrations.AddField(
            model_name='session',
            name='panel',
            field=models.ForeignKey(related_name='sessions', blank=True, to='api.Panel', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='panel',
            unique_together=set([('convention', 'kind')]),
        ),
    ]
