# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0142_award_qual_score'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='award',
            options={'ordering': ('-contest',)},
        ),
        migrations.AddField(
            model_name='award',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='awards', blank=True, to='api.Organization', null=True),
        ),
    ]
