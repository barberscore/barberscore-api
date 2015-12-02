# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0063_organization'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='convention',
            options={'ordering': ['organization', '-year']},
        ),
        migrations.AddField(
            model_name='contest',
            name='organization',
            field=models.ForeignKey(related_name='contests', blank=True, to='api.Organization', null=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='organization',
            field=models.ForeignKey(related_name='contestants', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Organization', null=True),
        ),
        migrations.AddField(
            model_name='convention',
            name='organization',
            field=models.ForeignKey(blank=True, to='api.Organization', help_text=b"\n            The district for the convention.  If International, this is 'BHS'.", null=True),
        ),
        migrations.AddField(
            model_name='judge',
            name='organization',
            field=models.ForeignKey(related_name='judges', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Organization', null=True),
        ),
    ]
