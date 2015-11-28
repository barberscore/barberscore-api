# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0128_auto_20151121_2347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, always_update=True, unique=True)),
                ('award', models.ForeignKey(related_name='rankings', to='api.Award')),
                ('contest', models.ForeignKey(related_name='rankings', to='api.Contest')),
                ('contestant', models.ForeignKey(related_name='rankings', to='api.Contestant')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='winner',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='winner',
            name='award',
        ),
        migrations.RemoveField(
            model_name='winner',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='winner',
            name='contestant',
        ),
        migrations.DeleteModel(
            name='Winner',
        ),
        migrations.AlterUniqueTogether(
            name='ranking',
            unique_together=set([('contestant', 'award')]),
        ),
    ]
