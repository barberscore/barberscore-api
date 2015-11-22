# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import autoslug.fields
import mptt.fields
import django.db.models.deletion
import apps.api.models
import django_fsm
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0128_auto_20151121_2347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrant',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('status', django_fsm.FSMIntegerField(default=0, choices=[(0, b'New'), (60, b'Finished'), (90, b'Final')])),
                ('status_monitor', model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status')),
                ('picture', models.ImageField(null=True, upload_to=apps.api.models.generate_image_filename, blank=True)),
                ('seed', models.IntegerField(null=True, blank=True)),
                ('prelim', models.FloatField(null=True, blank=True)),
                ('place', models.IntegerField(null=True, blank=True)),
                ('men', models.IntegerField(default=4, null=True, blank=True)),
                ('contest', models.ForeignKey(related_name='entrants', to='api.Contest')),
                ('group', models.ForeignKey(related_name='entrants', to='api.Group')),
                ('organization', mptt.fields.TreeForeignKey(related_name='entrants', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Organization', null=True)),
            ],
            options={
                'ordering': ('contest', 'group'),
            },
        ),
        migrations.AlterModelOptions(
            name='convention',
            options={'ordering': ['-year', 'kind', 'organization']},
        ),
        migrations.AddField(
            model_name='contestant',
            name='entrant',
            field=models.ForeignKey(related_name='contestants', blank=True, to='api.Entrant', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='entrant',
            unique_together=set([('group', 'contest')]),
        ),
    ]
