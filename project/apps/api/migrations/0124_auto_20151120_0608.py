# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0123_person_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('category', models.IntegerField(choices=[(0, b'Admin'), (1, b'Music'), (2, b'Presentation'), (3, b'Singing')])),
                ('status', models.IntegerField(choices=[(1, b'Active'), (2, b'Candidate')])),
                ('status_monitor', model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status')),
                ('person', models.ForeignKey(related_name='certifications', to='api.Person')),
            ],
        ),
        migrations.RemoveField(
            model_name='panelist',
            name='is_practice',
        ),
        migrations.AlterUniqueTogether(
            name='certification',
            unique_together=set([('category', 'person')]),
        ),
    ]
